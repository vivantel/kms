#!/usr/bin/env python3
"""
Fast token-economy fixer using translation table.
Applies mechanical phrase replacements without LLM.
"""

import re
import yaml
import sys
from pathlib import Path

def load_translation_table(path: str) -> list:
    """Load translation table from YAML."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get('translations', [])

def apply_translations(content: str, translations: list) -> tuple[str, list]:
    """Apply all translations to content. Returns (new_content, changes_made)."""
    changes = []
    new_content = content
    
    for t in translations:
        pattern = t['pattern']
        replacement = t['replacement']
        reason = t.get('reason', '')
        
        # Case-insensitive replacement
        matches = list(re.finditer(re.escape(pattern), new_content, re.IGNORECASE))
        if matches:
            count = len(matches)
            new_content = re.sub(re.escape(pattern), replacement, new_content, flags=re.IGNORECASE)
            changes.append({
                'pattern': pattern,
                'replacement': replacement,
                'count': count,
                'reason': reason
            })
    
    return new_content, changes

def fix_token_economy(file_path: str, translation_table_path: str) -> dict:
    """Fix token-economy violations in a file."""
    content = Path(file_path).read_text()
    translations = load_translation_table(translation_table_path)
    
    # Split frontmatter and body
    frontmatter = ''
    body = content
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            frontmatter = content[3:end]
            body = content[end+3:]
    
    # Apply translations only to body (not frontmatter)
    new_body, changes = apply_translations(body, translations)
    
    if changes:
        new_content = frontmatter
        if new_content:
            new_content = '---\n' + new_content + '---\n'
        new_content += new_body
        
        Path(file_path).write_text(new_content)
    
    return {
        'fixed': len(changes) > 0,
        'changes': changes,
        'total_replacements': sum(c['count'] for c in changes)
    }

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: fix_token_economy.py <file> <translation_table>", file=sys.stderr)
        sys.exit(1)
    
    result = fix_token_economy(sys.argv[1], sys.argv[2])
    print(yaml.dump(result))