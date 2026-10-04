#!/usr/bin/env python3
"""
Inline Lint Fix - Fixes mechanical lint violations directly without spawning opencode agents.
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple


class InlineFixer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.canonical_tags: Set[str] = set()
        self.known_ids: Dict[str, Path] = {}
        self.translation_table: List[Dict] = []
        self.changes_made = []

    def load_canonical_tags(self):
        tags_file = self.repo_root / "docs" / "skills" / "tags.md"
        if tags_file.exists():
            content = tags_file.read_text()
            for line in content.split('\n'):
                match = re.match(r'^-\s+(\S+):', line)
                if match:
                    self.canonical_tags.add(match.group(1))

    def load_known_ids(self):
        for type_dir in ["facts", "decisions", "guardrails", "skills"]:
            dir_path = self.repo_root / "docs" / type_dir
            if dir_path.exists():
                for md_file in dir_path.glob("*.md"):
                    if "archive" not in md_file.parts:
                        self._extract_id_from_file(md_file, type_dir)
        for skill_dir in (self.repo_root / "plugins" / "kms" / "skills").glob("*"):
            if skill_dir.is_dir():
                for md_file in skill_dir.glob("*.md"):
                    self._extract_id_from_file(md_file, "skill")

    def _extract_id_from_file(self, file_path: Path, type_hint: str):
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

    def load_translation_table(self):
        table_path = self.repo_root / "plugins" / "kms" / "hooks" / "translation_table.yaml"
        if table_path.exists():
            try:
                with open(table_path) as f:
                    data = yaml.safe_load(f)
                self.translation_table = data.get('translations', [])
            except Exception:
                pass

    def fix_file(self, file_path: str, violations: List[Dict]) -> Tuple[bool, str]:
        """Fix all violations in a file. Returns (fixed, changes_description)."""
        full_path = self.repo_root / file_path
        if not full_path.exists():
            return False, f"File not found: {file_path}"

        try:
            content = full_path.read_text()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        original_content = content
        self.changes_made = []
        self.current_file = file_path  # Store for _default_value

        # Parse frontmatter
        frontmatter = {}
        self.frontmatter_order = []  # Track original field order
        body = content
        frontmatter_end = 0
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                try:
                    fm_text = content[3:end].strip()
                    frontmatter = yaml.safe_load(fm_text) or {}
                    # Extract field order from original YAML
                    for line in fm_text.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Match key: value or key:
                            match = re.match(r'^(\w[\w-]*):', line)
                            if match:
                                key = match.group(1)
                                if key not in self.frontmatter_order:
                                    self.frontmatter_order.append(key)
                    body = content[end+3:]
                    frontmatter_end = end + 3
                except Exception:
                    pass

        # Determine artifact type
        artifact_type = self._get_artifact_type(file_path)

        # Group violations by type
        by_type = {}
        for v in violations:
            vtype = v['type']
            if vtype not in by_type:
                by_type[vtype] = []
            by_type[vtype].append(v)

        # Apply fixes in order
        if 'structure' in by_type:
            content = self._fix_structure(content, frontmatter, artifact_type, by_type['structure'], frontmatter_end)
            # Re-parse frontmatter after structure fixes
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    fm_text = content[3:end].strip()
                    frontmatter = yaml.safe_load(fm_text) or {}
                    # Re-extract field order
                    self.frontmatter_order = []
                    for line in fm_text.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            match = re.match(r'^(\w[\w-]*):', line)
                            if match:
                                key = match.group(1)
                                if key not in self.frontmatter_order:
                                    self.frontmatter_order.append(key)
                    body = content[end+3:]
                    frontmatter_end = end + 3

        if 'format' in by_type:
            content = self._fix_format(content, frontmatter, artifact_type, by_type['format'], frontmatter_end)
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    fm_text = content[3:end].strip()
                    frontmatter = yaml.safe_load(fm_text) or {}
                    self.frontmatter_order = []
                    for line in fm_text.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            match = re.match(r'^(\w[\w-]*):', line)
                            if match:
                                key = match.group(1)
                                if key not in self.frontmatter_order:
                                    self.frontmatter_order.append(key)
                    body = content[end+3:]
                    frontmatter_end = end + 3

        if 'tags' in by_type:
            content = self._fix_tags(content, frontmatter, by_type['tags'], frontmatter_end)
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    fm_text = content[3:end].strip()
                    frontmatter = yaml.safe_load(fm_text) or {}
                    self.frontmatter_order = []
                    for line in fm_text.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            match = re.match(r'^(\w[\w-]*):', line)
                            if match:
                                key = match.group(1)
                                if key not in self.frontmatter_order:
                                    self.frontmatter_order.append(key)
                    body = content[end+3:]
                    frontmatter_end = end + 3

        if 'xref' in by_type:
            content = self._fix_xrefs(content, frontmatter, body, by_type['xref'], frontmatter_end)
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    fm_text = content[3:end].strip()
                    frontmatter = yaml.safe_load(fm_text) or {}
                    self.frontmatter_order = []
                    for line in fm_text.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            match = re.match(r'^(\w[\w-]*):', line)
                            if match:
                                key = match.group(1)
                                if key not in self.frontmatter_order:
                                    self.frontmatter_order.append(key)
                    body = content[end+3:]
                    frontmatter_end = end + 3

        if 'token-economy' in by_type:
            content = self._fix_token_economy(content, body, by_type['token-economy'])

        if 'derivation' in by_type:
            content = self._fix_derivation(content, frontmatter, by_type['derivation'], frontmatter_end)

        # Write if changed
        if content != original_content:
            full_path.write_text(content)
            return True, "; ".join(self.changes_made)
        return False, "No changes needed"

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

    def _build_frontmatter(self, fm: Dict, artifact_type: str, file_path: Optional[str] = None, field_order: Optional[List[str]] = None) -> List[str]:
        """Build a new frontmatter with all required fields, preserving original field order."""
        new_fm = fm.copy()
        required_base = ['id', 'title', 'status', 'date', 'tags']
        for field in required_base:
            if field not in new_fm:
                new_fm[field] = self._default_value(field, artifact_type, file_path)
        type_required = {
            'fact': ['kind', 'governed-by'],
            'guardrail': ['governed-by', 'grounded-in', 'derivation-note'],
            'decision': ['track'],
        }
        if artifact_type in type_required:
            for field in type_required[artifact_type]:
                if field not in new_fm:
                    new_fm[field] = self._default_value(field, artifact_type, file_path)
        
        # Determine output order: original order first, then new fields
        output_order = list(field_order) if field_order else []
        for key in new_fm.keys():
            if key not in output_order:
                output_order.append(key)
        
        fm_lines = ['---']
        for key in output_order:
            if key not in new_fm:
                continue
            value = new_fm[key]
            if isinstance(value, list):
                if value:
                    fm_lines.append(f"{key}:")
                    for item in value:
                        fm_lines.append(f"  - {item}")
                else:
                    fm_lines.append(f"{key}: []")
            else:
                fm_lines.append(f"{key}: {value}")
        fm_lines.append('---')
        return fm_lines

    def _fix_structure(self, content: str, fm: Dict, artifact_type: str, violations: List[Dict], fm_end: int) -> str:
        """Fix structure violations: missing required fields."""
        lines = content.split('\n')
        
        # Find frontmatter boundaries
        fm_start = -1
        fm_end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if fm_start == -1:
                    fm_start = i
                else:
                    fm_end_idx = i
                    break
        
        if fm_start == -1 or fm_end_idx == -1:
            # No frontmatter - add one
            new_fm = self._build_frontmatter(fm, artifact_type, self.current_file, getattr(self, 'frontmatter_order', None))
            # Track what was added
            required_base = ['id', 'title', 'status', 'date', 'tags']
            for field in required_base:
                if field not in fm:
                    self.changes_made.append(f"Added missing field: {field}")
            type_required = {
                'fact': ['kind', 'governed-by'],
                'guardrail': ['governed-by', 'grounded-in', 'derivation-note'],
                'decision': ['track'],
            }
            if artifact_type in type_required:
                for field in type_required[artifact_type]:
                    if field not in fm:
                        self.changes_made.append(f"Added missing field for {artifact_type}: {field}")
            # Strip any leading --- from body to avoid duplicate frontmatter markers
            body_lines = lines
            # Remove any leading '---' lines from body (could be from code blocks)
            while body_lines and body_lines[0].strip() == '---':
                body_lines = body_lines[1:]
            return '\n'.join(new_fm + [''] + body_lines)
        
        # Build new frontmatter with all required fields
        new_fm_dict = fm.copy()
        
        # Base required fields
        required_base = ['id', 'title', 'status', 'date', 'tags']
        for field in required_base:
            if field not in new_fm_dict:
                new_fm_dict[field] = self._default_value(field, artifact_type, self.current_file)
                self.changes_made.append(f"Added missing field: {field}")
        
        # Type-specific required fields
        type_required = {
            'fact': ['kind', 'governed-by'],
            'guardrail': ['governed-by', 'grounded-in', 'derivation-note'],
            'decision': ['track'],
        }
        if artifact_type in type_required:
            for field in type_required[artifact_type]:
                if field not in new_fm_dict:
                    new_fm_dict[field] = self._default_value(field, artifact_type, self.current_file)
                    self.changes_made.append(f"Added missing field for {artifact_type}: {field}")
        
        # Fix list fields
        list_fields = ['grounded-in', 'governed-by', 'governed-facts', 'operationalizes', 'tags']
        for field in list_fields:
            if field in new_fm_dict and not isinstance(new_fm_dict[field], list):
                val = new_fm_dict[field]
                new_fm_dict[field] = [val] if val else []
                self.changes_made.append(f"Fixed {field} to be a list")
        
        # Fix status value
        valid_status = {'draft', 'active', 'superseded', 'deprecated'}
        if 'status' in new_fm_dict and new_fm_dict['status'] not in valid_status:
            new_fm_dict['status'] = 'draft'
            self.changes_made.append(f"Fixed invalid status to 'draft'")
        
        # Rebuild frontmatter section using _build_frontmatter to preserve order
        fm_lines = self._build_frontmatter(new_fm_dict, artifact_type, self.current_file, self.frontmatter_order)
        
        # Replace frontmatter in content
        body_lines = lines[fm_end_idx + 1:]
        return '\n'.join(fm_lines + body_lines)

    def _default_value(self, field: str, artifact_type: str, file_path: Optional[str] = None) -> Any:
        defaults = {
            'id': 'TBD',
            'title': 'TBD',
            'status': 'draft',
            'date': '2026-01-01',
            'tags': [],
            'kind': 'reference',
            'governed-by': [],
            'grounded-in': [],
            'derivation-note': 'TBD',
            'track': 'product',
        }
        
        # Generate ID from file path if available
        if field == 'id' and file_path:
            # Extract base name without extension
            base = Path(file_path).stem
            # Remove common suffixes
            base = base.replace('-fact', '').replace('-decision', '').replace('-guardrail', '').replace('-skill', '')
            # Sanitize: lowercase, replace non-alphanumeric with dash
            generated_id = re.sub(r'[^a-z0-9]+', '-', base.lower()).strip('-')
            if generated_id:
                return generated_id
        
        # Generate title from file path if available
        if field == 'title' and file_path:
            base = Path(file_path).stem
            # Convert kebab-case to Title Case
            title = ' '.join(word.capitalize() for word in base.replace('-', ' ').split())
            if title:
                return title
        
        return defaults.get(field, '')

    def _fix_format(self, content: str, fm: Dict, artifact_type: str, violations: List[Dict], fm_end: int) -> str:
        """Fix format violations: INDEX.md sync, YAML syntax."""
        # For now, just handle INDEX.md missing violations by noting they need manual INDEX update
        for v in violations:
            msg = v.get('message', '')
            if 'missing from' in msg and 'INDEX.md' in msg:
                self.changes_made.append(f"Note: {msg} (requires manual INDEX.md update)")
        return content

    def _fix_tags(self, content: str, fm: Dict, violations: List[Dict], fm_end: int) -> str:
        """Fix tags violations: non-canonical tags."""
        if not self.canonical_tags:
            return content
        
        lines = content.split('\n')
        fm_start = -1
        fm_end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if fm_start == -1:
                    fm_start = i
                else:
                    fm_end_idx = i
                    break
        
        if fm_start == -1 or fm_end_idx == -1:
            return content
        
        # Parse current tags
        current_tags = fm.get('tags', [])
        if isinstance(current_tags, str):
            current_tags = [current_tags]
        elif not isinstance(current_tags, list):
            current_tags = []
        
        # Filter to canonical tags
        new_tags = [t for t in current_tags if t in self.canonical_tags]
        if len(new_tags) != len(current_tags):
            # Rebuild frontmatter with fixed tags using _build_frontmatter to preserve order
            new_fm = fm.copy()
            new_fm['tags'] = new_tags
            self.changes_made.append(f"Removed non-canonical tags: {set(current_tags) - set(new_tags)}")
            
            artifact_type = self._get_artifact_type(self.current_file)
            fm_lines = self._build_frontmatter(new_fm, artifact_type, self.current_file, self.frontmatter_order)
            body_lines = lines[fm_end_idx + 1:]
            return '\n'.join(fm_lines + body_lines)
        
        return content

    def _fix_xrefs(self, content: str, fm: Dict, body: str, violations: List[Dict], fm_end: int) -> str:
        """Fix xref violations: dangling references."""
        # For now, just note them - fixing requires human judgment
        for v in violations:
            msg = v.get('message', '')
            self.changes_made.append(f"Note: {msg} (requires human judgment)")
        return content

    def _fix_token_economy(self, content: str, body: str, violations: List[Dict]) -> str:
        """Fix token economy violations: long sentences, redundant phrases, restatements."""
        new_content = content
        
        # Apply translation table replacements (case-insensitive)
        for t in self.translation_table:
            pattern = t.get('pattern', '')
            replacement = t.get('replacement', '')
            if pattern and replacement:
                # Use re.IGNORECASE for case-insensitive matching, re.escape for literal pattern
                new_content, count = re.subn(re.escape(pattern), replacement, new_content, flags=re.IGNORECASE)
                if count > 0:
                    self.changes_made.append(f"Replaced '{pattern}' → '{replacement}' ({count} occurrences)")
        
        # For long sentences and restatements, we'd need more sophisticated parsing
        # For now, just note them
        for v in violations:
            msg = v.get('message', '')
            if 'words (>40)' in msg:
                self.changes_made.append(f"Note: {msg} (requires manual rewrite)")
            elif 'restatement' in msg.lower():
                self.changes_made.append(f"Note: {msg} (requires manual rewrite)")
        
        return new_content

    def _fix_derivation(self, content: str, fm: Dict, violations: List[Dict], fm_end: int) -> str:
        """Fix derivation violations: missing governed-by, grounded-in, derivation-note."""
        lines = content.split('\n')
        fm_start = -1
        fm_end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if fm_start == -1:
                    fm_start = i
                else:
                    fm_end_idx = i
                    break
        
        if fm_start == -1 or fm_end_idx == -1:
            return content
        
        new_fm = fm.copy()
        for v in violations:
            msg = v.get('message', '')
            if 'Missing required field' in msg:
                # Extract field name - handles both "field for X: Y" and "field: Y" formats
                match = re.search(r"field(?: for \w+)?:\s*(\w[\w-]*)", msg)
                if match:
                    field = match.group(1)
                    if field not in new_fm:
                        new_fm[field] = self._default_value(field, self._get_artifact_type(self.current_file), self.current_file)
                        self.changes_made.append(f"Added missing derivation field: {field}")
        
        if new_fm != fm:
            artifact_type = self._get_artifact_type(self.current_file)
            fm_lines = self._build_frontmatter(new_fm, artifact_type, self.current_file, self.frontmatter_order)
            body_lines = lines[fm_end_idx + 1:]
            return '\n'.join(fm_lines + body_lines)
        
        return content


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--file', required=True)
    parser.add_argument('--violations', required=True, help='JSON array of violations')
    args = parser.parse_args()

    violations = json.loads(args.violations)
    fixer = InlineFixer(args.repo_root)
    fixer.load_canonical_tags()
    fixer.load_known_ids()
    fixer.load_translation_table()
    
    fixed, changes = fixer.fix_file(args.file, violations)
    
    result = {
        "fixed": fixed,
        "changes": changes,
        "semantic_hash": "",  # Could compute if needed
        "retries": 0
    }
    if not fixed:
        result["reason"] = changes
    
    print(json.dumps(result))


if __name__ == '__main__':
    main()