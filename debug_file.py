#!/usr/bin/env python3
import os

file_path = r"guides\raw_transcripts\1. 95% of Pots are Multiway.txt"

print(f"File exists: {os.path.exists(file_path)}")
print(f"File size: {os.path.getsize(file_path)} bytes")

# Try different encodings
encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

for encoding in encodings:
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        print(f"Successfully read with {encoding}: {len(content)} characters")
        if len(content) > 0:
            print(f"First 100 characters: {repr(content[:100])}")
            break
    except Exception as e:
        print(f"Failed with {encoding}: {e}")
