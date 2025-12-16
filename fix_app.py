#!/usr/bin/env python
# Script to fix app.py by removing duplicate class definitions

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep lines 1-360 (everything up to and including the corrected animate_text)
# Skip lines 361-634 (duplicate class definitions)  
# Keep lines 635 onwards (load_node and rest of file)

fixed_lines = lines[:360] + lines[634:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Fixed! Removed {634-360} duplicate lines.")
print(f"New file has {len(fixed_lines)} lines (was {len(lines)})")
