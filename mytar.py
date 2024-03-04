#!/usr/bin/env python3
import sys
import os

def create_archive_outband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            # Use the filename directly in the current directory
            with open(filename, 'rb') as f:
                content = f.read()
                header = f"{filename}:{len(content)}:".encode()
                archive.write(header + content)

def extract_archive_outband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()
        while content:
            pos = content.find(b':')
            filename = content[:pos].decode()
            content = content[pos+1:]
            pos = content.find(b':')
            size = int(content[:pos])
            content = content[pos+1:]
            file_content = content[:size]
            content = content[size:]
            # Extract files to the current directory
            with open(filename, 'wb') as f:
                f.write(file_content)

#Inband Framer and Outband Framer Implementation


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: mytar.py [i|o] [c|x] [archive_name] [files...]", file=sys.stderr)
        sys.exit(1)

    type_extract = sys.argv[1]
    operation = sys.argv[2]
    archive_name = sys.argv[3]  # Use the given path directly without converting to absolute path

    if operation == "c" and type_extract == "o":
        files_to_archive = sys.argv[4:]
        create_archive_outband(archive_name, files_to_archive)
    elif operation == "x" and type_extract == "o":
        extract_archive_outband(archive_name)
    else:
        print(f"Unknown operation: {operation}", file=sys.stderr)
        sys.exit(1)
