#!/usr/bin/env python3
"""
KMS Lint Checker - Fast automated lint checks for KMS knowledge artifacts.
Outputs violations as JSON for the improvement harness.
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

class KMSLintChecker:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.violations = []
        self.files_checked = 0
        self.known_ids: Dict[str, Path] = {}  # id -> file path
        self.canonical_tags: Set[str] = set()
        self.index_data: Dict[str, List[Dict]] = {}  # type -> list of rows

    def load_canonical_tags(self):
        """Load canonical tags from docs/skills/tags.md"""
        tags_file = self.repo_root / "docs" / "skills" / "tags.md"
        if tags_file.exists():
            content = tags_file.read_text()
            # Parse tags from the file - look for lines like "- tag-name: description"
            for line in content.split('\n'):
                match = re.match(r'^-\s+(\S+):', line)
                if match:
                    self.canonical_tags.add(match.group(1))

    def load_known_ids(self):
        """Load all known artifact IDs from the knowledge base"""
        # Scan docs/facts, docs/decisions, docs/guardrails, docs/skills
        for type_dir in ["facts", "decisions", "guardrails", "skills"]:
            dir_path = self.repo_root / "docs" / type_dir
            if dir_path.exists():
                for md_file in dir_path.glob("*.md"):
                    if "archive" not in md_file.parts:
                        self._extract_id_from_file(md_file, type_dir)
        
        # Also scan plugins/kms/skills/**/SKILL.md and examples.md
        for skill_dir in (self.repo_root / "plugins" / "kms" / "skills").glob("*"):
            if skill_dir.is_dir():
                for md_file in skill_dir.glob("*.md"):
                    self._extract_id_from_file(md_file, "skill")

    def _extract_id_from_file(self, file_path: Path, type_hint: str):
        """Extract ID from frontmatter"""
        try:
            content = file_path.read_text()
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    frontmatter = content[3:end].strip()
                    data = yaml.safe_load(frontmatter)
                    if data and 'id' in data:
                        self.known_ids[data['id']] = file_path
        except Exception:
            pass

    def load_index_data(self):
        """Load INDEX.md files for sync checking"""
        for type_dir in ["facts", "decisions", "guardrails", "skills"]:
            for index_path in [
                self.repo_root / "docs" / type_dir / "INDEX.md",
                self.repo_root / "docs" / type_dir / "archive" / "INDEX.md"
            ]:
                if index_path.exists():
                    self._parse_index(index_path, type_dir)

    def _parse_index(self, index_path: Path, type_name: str):
        """Parse CSV INDEX.md"""
        try:
            content = index_path.read_text()
            lines = content.strip().split('\n')
            if len(lines) < 2:
                return
            header = [h.strip() for h in lines[0].split(',')]
            rows = []
            for line in lines[1:]:
                # Simple CSV parse - handles quoted fields
                fields = []
                field = ''
                in_quotes = False
                for char in line:
                    if char == '"' and not in_quotes:
                        in_quotes = True
                    elif char == '"' and in_quotes:
                        in_quotes = False
                    elif char == ',' and not in_quotes:
                        fields.append(field.strip())
                        field = ''
                    else:
                        field += char
                fields.append(field.strip())
                if len(fields) == len(header):
                    rows.append(dict(zip(header, fields)))
            self.index_data[type_name] = rows
        except Exception:
            pass

    def check_file(self, file_path: Path, rel_path: str):
        """Run all lint checks on a single file"""
        self.files_checked += 1
        try:
            content = file_path.read_text()
        except Exception as e:
            self._add_violation(rel_path, "format", f"Failed to read file: {e}", 0)
            return

        # Parse frontmatter
        frontmatter = {}
        body = content
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                try:
                    frontmatter = yaml.safe_load(content[3:end].strip()) or {}
                    body = content[end+3:]
                except Exception as e:
                    self._add_violation(rel_path, "format", f"Invalid YAML frontmatter: {e}", 0)
                    return

        # Determine artifact type from path
        artifact_type = self._get_artifact_type(rel_path)

        # Run checks
        self._check_required_fields(rel_path, frontmatter, artifact_type)
        self._check_status_values(rel_path, frontmatter)
        self._check_list_fields(rel_path, frontmatter)
        self._check_dangling_references(rel_path, frontmatter)
        self._check_tags(rel_path, frontmatter)
        self._check_verbose_artifacts(rel_path, body, artifact_type)
        self._check_stale_prose_refs(rel_path, body)
        self._check_index_sync(rel_path, frontmatter, artifact_type)

    def _get_artifact_type(self, rel_path: str) -> str:
        if rel_path.startswith("docs/facts/"):
            return "fact"
        elif rel_path.startswith("docs/decisions/"):
            return "decision"
        elif rel_path.startswith("docs/guardrails/"):
            return "guardrail"
        elif rel_path.startswith("docs/skills/"):
            return "procedure"
        elif rel_path.startswith("plugins/kms/skills/"):
            if rel_path.endswith("SKILL.md"):
                return "skill"
            return "procedure"
        return "unknown"

    def _check_required_fields(self, rel_path: str, fm: Dict, artifact_type: str):
        required_base = ['id', 'title', 'status', 'date', 'tags']
        for field in required_base:
            if field not in fm:
                self._add_violation(rel_path, "structure", f"Missing required field: {field}", 0)

        type_required = {
            'fact': ['kind', 'governed-by'],
            'guardrail': ['governed-by', 'grounded-in', 'derivation-note'],
            'decision': ['track'],
        }
        if artifact_type in type_required:
            for field in type_required[artifact_type]:
                if field not in fm:
                    self._add_violation(rel_path, "structure", f"Missing required field for {artifact_type}: {field}", 0)

    def _check_status_values(self, rel_path: str, fm: Dict):
        valid_status = {'draft', 'active', 'superseded', 'deprecated'}
        if 'status' in fm and fm['status'] not in valid_status:
            self._add_violation(rel_path, "structure", f"Invalid status value: {fm['status']} (must be one of {valid_status})", 0)

        if fm.get('status') == 'superseded' and 'superseded-by' not in fm:
            self._add_violation(rel_path, "structure", "Status is 'superseded' but missing 'superseded-by' field", 0)

    def _check_list_fields(self, rel_path: str, fm: Dict):
        list_fields = ['grounded-in', 'governed-facts', 'operationalizes']
        for field in list_fields:
            if field in fm and not isinstance(fm[field], list):
                self._add_violation(rel_path, "structure", f"Field '{field}' must be a YAML list, not {type(fm[field]).__name__}", 0)

    def _check_dangling_references(self, rel_path: str, fm: Dict):
        ref_fields = ['governed-by', 'grounded-in', 'superseded-by', 'governed-facts', 'operationalizes']
        for field in ref_fields:
            if field not in fm:
                continue
            refs = fm[field]
            if isinstance(refs, str):
                refs = [refs]
            elif not isinstance(refs, list):
                continue
            for ref in refs:
                if ref and ref != "TBD" and ref not in self.known_ids:
                    self._add_violation(rel_path, "xref", f"Dangling reference in {field}: '{ref}' not found", 0)

    def _check_tags(self, rel_path: str, fm: Dict):
        if not self.canonical_tags:
            return
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        elif not isinstance(tags, list):
            return
        for tag in tags:
            if tag not in self.canonical_tags:
                self._add_violation(rel_path, "tags", f"Tag '{tag}' not in canonical list (docs/skills/tags.md)", 0)

    def _check_verbose_artifacts(self, rel_path: str, body: str, artifact_type: str):
        # Skip decisions and plans
        if artifact_type in ('decision', 'plan'):
            return
        
        # Split into paragraphs, exclude markdown list items from sentence analysis
        # A "sentence" for our purposes is prose text, not list items
        prose_lines = []
        for line in body.split('\n'):
            stripped = line.strip()
            # Skip markdown list items, code blocks, headers
            if (stripped.startswith('- ') or 
                stripped.startswith('* ') or
                re.match(r'^\d+\.\s', stripped) or
                stripped.startswith('```') or
                stripped.startswith('#')):
                continue
            prose_lines.append(line)
        prose = '\n'.join(prose_lines)
        
        # Check for restatement - same sentence structure repeated
        sentences = re.split(r'[.!?]\s+', prose)
        seen_starts = {}
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if len(sent) < 20:
                continue
            start = sent[:50].lower()
            if start in seen_starts:
                self._add_violation(rel_path, "token-economy", f"Possible restatement: sentence {i+1} similar to sentence {seen_starts[start]+1}", 0)
            else:
                seen_starts[start] = i
        # Check for long sentences
        for i, sent in enumerate(sentences):
            words = len(sent.split())
            if words > 40:
                self._add_violation(rel_path, "token-economy", f"Sentence {i+1} has {words} words (>40)", 0)
        # Check for redundant phrases using translation table
        translations = self._load_translation_table()
        for t in translations:
            pattern = t['pattern']
            replacement = t['replacement']
            if re.search(re.escape(pattern), body, re.IGNORECASE):
                self._add_violation(rel_path, "token-economy", f"Redundant phrase: '{pattern}' → '{replacement}'", 0)

    def _load_translation_table(self) -> list:
        """Load translation table from YAML."""
        table_path = self.repo_root / "plugins" / "kms" / "hooks" / "translation_table.yaml"
        if not table_path.exists():
            return []
        try:
            with open(table_path) as f:
                data = yaml.safe_load(f)
            return data.get('translations', [])
        except Exception:
            return []

    def _check_stale_prose_refs(self, rel_path: str, body: str):
        # Find inline references to docs/ paths
        refs = re.findall(r'docs/(facts|decisions|guardrails|skills)/([\w\-]+\.md)', body)
        for type_name, filename in refs:
            ref_path = self.repo_root / "docs" / type_name / filename
            if not ref_path.exists():
                # Check archive too
                archive_path = self.repo_root / "docs" / type_name / "archive" / filename
                if not archive_path.exists():
                    self._add_violation(rel_path, "xref", f"Stale prose reference: docs/{type_name}/{filename} not found", 0)

    def _check_index_sync(self, rel_path: str, fm: Dict, artifact_type: str):
        type_map = {
            'fact': 'facts',
            'decision': 'decisions',
            'guardrail': 'guardrails',
            'procedure': 'skills',
            'skill': 'skills',
        }
        if artifact_type not in type_map:
            return
        index_type = type_map[artifact_type]
        if index_type not in self.index_data:
            return
        
        file_id = fm.get('id')
        if not file_id:
            return
        
        # Check if this file has a row in INDEX.md
        found = False
        for row in self.index_data[index_type]:
            if row.get('id') == file_id:
                found = True
                # Check if fields match
                for field in ['title', 'tags', 'status']:
                    if field in fm and field in row:
                        fm_val = fm[field]
                        row_val = row[field]
                        if isinstance(fm_val, list):
                            fm_val = ', '.join(fm_val)
                        if str(fm_val) != str(row_val):
                            self._add_violation(rel_path, "format", f"INDEX.md mismatch for {field}: frontmatter='{fm_val}' index='{row_val}'", 0)
                break
        
        if not found:
            self._add_violation(rel_path, "format", f"File missing from {index_type}/INDEX.md", 0)

    def _add_violation(self, file: str, vtype: str, message: str, line: int):
        self.violations.append({
            "file": file,
            "type": vtype,
            "message": message,
            "line": line,
            "suggestion": ""
        })

    def discover_files(self, scope: str, target: Optional[str] = None) -> List[Path]:
        """Discover files to lint"""
        files = []
        if scope == "file" and target:
            files.append(self.repo_root / target)
        else:
            # All knowledge artifacts
            patterns = [
                "docs/facts/*.md",
                "docs/decisions/*.md",
                "docs/guardrails/*.md",
                "docs/skills/*.md",
                "plugins/kms/skills/**/SKILL.md",
                "plugins/kms/skills/**/examples.md",
            ]
            for pattern in patterns:
                for f in self.repo_root.glob(pattern):
                    if "archive" not in f.parts:
                        files.append(f)
        return files

    def run(self, scope: str = "all", target: Optional[str] = None) -> Dict:
        """Run lint checks"""
        self.load_canonical_tags()
        self.load_known_ids()
        self.load_index_data()

        files = self.discover_files(scope, target)
        for f in files:
            try:
                rel = f.relative_to(self.repo_root)
            except ValueError:
                rel = f
            self.check_file(f, str(rel))

        return {
            "violations": self.violations,
            "summary": {
                "files_checked": self.files_checked,
                "total_violations": len(self.violations),
                "by_type": self._count_by_type()
            }
        }

    def _count_by_type(self) -> Dict[str, int]:
        counts = {}
        for v in self.violations:
            counts[v['type']] = counts.get(v['type'], 0) + 1
        return counts


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scope', choices=['all', 'file'], default='all')
    parser.add_argument('--target', help='File path when scope=file')
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()

    checker = KMSLintChecker(args.repo_root)
    result = checker.run(args.scope, args.target)
    
    print(json.dumps(result, indent=2))
    
    # Exit code: 0 if no violations, 1 if violations found
    sys.exit(1 if result['summary']['total_violations'] > 0 else 0)


if __name__ == '__main__':
    main()