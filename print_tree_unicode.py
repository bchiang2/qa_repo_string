#!/usr/bin/env python3
"""
Print directory tree with Unicode codepoints for each filename.
Useful for detecting hidden/special Unicode characters in filenames.
"""

import os
import sys


def char_to_codepoint(char: str) -> str:
    """Convert a character to its Unicode codepoint representation."""
    cp = ord(char)
    if cp < 0x100:
        return f"U+{cp:04X}"
    else:
        return f"U+{cp:04X}"


def filename_with_codepoints(name: str) -> str:
    """Return filename with Unicode codepoints for each character."""
    codepoints = [char_to_codepoint(c) for c in name]
    return f"{name!r} [{' '.join(codepoints)}]"


def print_tree(root: str, prefix: str = "", ignore_hidden: bool = True, ignore_git: bool = True):
    """Print directory tree with Unicode codepoints."""
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
        return

    # Filter entries
    if ignore_hidden:
        entries = [e for e in entries if not e.startswith('.')]
    if ignore_git:
        entries = [e for e in entries if e != '.git']

    dirs = []
    files = []
    
    for entry in entries:
        path = os.path.join(root, entry)
        if os.path.isdir(path):
            dirs.append(entry)
        else:
            files.append(entry)

    # Print files first, then directories
    all_entries = files + dirs
    
    for i, entry in enumerate(all_entries):
        is_last = (i == len(all_entries) - 1)
        connector = "└── " if is_last else "├── "
        
        path = os.path.join(root, entry)
        is_dir = os.path.isdir(path)
        
        # Check if filename has non-ASCII or special Unicode
        has_special = any(ord(c) > 127 or ord(c) < 32 for c in entry)
        
        if has_special:
            # Show with codepoints for special characters
            print(f"{prefix}{connector}{filename_with_codepoints(entry)}{'/' if is_dir else ''}")
        else:
            print(f"{prefix}{connector}{entry}{'/' if is_dir else ''}")
        
        if is_dir:
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension, ignore_hidden, ignore_git)


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "."
    
    root = os.path.abspath(root)
    print(f"📁 {root}")
    print()
    print_tree(root)
    print()
    print("Legend: Files with special Unicode show as 'name' [U+XXXX U+XXXX ...]")


if __name__ == "__main__":
    main()

