import os
import re

exclude_dirs = {'node_modules', 'dist', '.git', '.github', '.gemini', 'locales'}
exclude_files = {'find_unlocalized.py', 'audit_localization.py', 'package-lock.json'}

# Regex for matches:
# Armenian characters: [Ա-Ֆա-ֆ]
armenian_regex = re.compile(r'[\u0531-\u0556\u0561-\u0587\u0589\u058a]')

# Let's search inside the src folder and its subdirectories
search_dir = './src'

unlocalized_matches = []

for root, dirs, files in os.walk(search_dir):
    # filter out excluded dirs
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file in exclude_files or 'i18n' in file:
            continue
        filepath = os.path.join(root, file)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for idx, line in enumerate(lines):
                    # check for Armenian chars
                    if armenian_regex.search(line):
                        # skip comments
                        stripped_line = line.strip()
                        if stripped_line.startswith('//') or stripped_line.startswith('/*') or stripped_line.startswith('*'):
                            continue
                        unlocalized_matches.append({
                            'file': filepath,
                            'line': idx + 1,
                            'content': stripped_line
                        })
        except Exception as e:
            pass

print(f"FOUND {len(unlocalized_matches)} ENTIRELY OR PARTIALLY UNLOCALIZED ARMENIAN LINES:")
for m in unlocalized_matches[:100]:
    print(f"FILE: {m['file']} | LINE: {m['line']} | CONTENT: {m['content']}")
if len(unlocalized_matches) > 100:
    print(f"... and {len(unlocalized_matches) - 100} more")
