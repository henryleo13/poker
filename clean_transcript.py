#!/usr/bin/env python3
"""
Script to clean up poker transcripts by removing timestamps and structuring content.
"""

import re
import os

def clean_transcript(input_file, output_file):
    """Clean transcript by removing timestamps and structuring content."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines
    lines = content.split('\n')
    
    cleaned_lines = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check if line is a timestamp (format: MM:SS or M:SS)
        if re.match(r'^\d{1,2}:\d{2}$', line):
            continue
            
        # Check if line is a section header (single word, no punctuation, capitalized)
        if re.match(r'^[A-Z][a-z]+$', line) and len(line) > 3:
            if current_section:
                cleaned_lines.append("")  # Add spacing between sections
            cleaned_lines.append(f"## {line}")
            current_section = line
            continue
            
        # Regular content line
        if line:
            cleaned_lines.append(line)
    
    # Join lines and clean up extra whitespace
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Clean up multiple consecutive empty lines
    cleaned_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_content)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

def process_all_transcripts():
    """Process all raw transcripts that haven't been converted yet."""
    
    raw_dir = "guides/raw_transcripts"
    fixed_dir = "guides/fixed_transcripts"
    
    # Create output directory if it doesn't exist
    os.makedirs(fixed_dir, exist_ok=True)
    
    # Get list of raw transcript files
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.txt')]
    
    # Get list of already processed files
    fixed_files = [f for f in os.listdir(fixed_dir) if f.endswith('.txt')] if os.path.exists(fixed_dir) else []
    
    print(f"Found {len(raw_files)} raw transcript files")
    print(f"Found {len(fixed_files)} already processed files")
    
    # Process files that haven't been converted yet
    for raw_file in raw_files:
        if raw_file not in fixed_files:
            input_path = os.path.join(raw_dir, raw_file)
            output_path = os.path.join(fixed_dir, raw_file)
            
            print(f"\nProcessing: {raw_file}")
            print(f"Input: {input_path}")
            print(f"Output: {output_path}")
            
            try:
                clean_transcript(input_path, output_path)
                print(f"✓ Successfully processed {raw_file}")
            except Exception as e:
                print(f"✗ Error processing {raw_file}: {e}")
        else:
            print(f"⏭ Skipping {raw_file} (already processed)")

if __name__ == "__main__":
    process_all_transcripts()
