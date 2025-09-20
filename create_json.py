#!/usr/bin/env python3
"""
Convert fixed poker transcripts to structured JSON guidelines using LLM.
Supports multiple LLM providers: OpenAI, Anthropic, or local models.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set environment variables manually.")

# Configuration
FIXED_DIR = Path("guides/fixed_transcripts")
OUTPUT_FILE = Path("guides/poker_guidelines.json")
CHUNK_SIZE = 2000  # Adjust based on your LLM's context window
OVERLAP = 200

# LLM Configuration - Choose one
LLM_PROVIDER = "anthropic"  # Options: "openai", "anthropic", "local"
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def create_guideline_prompt(transcript_chunk: str) -> str:
    """Create a prompt for extracting poker guidelines from transcript."""
    return f"""
You are an expert poker coach analyzing a transcript. Extract actionable poker guidelines and convert them to structured JSON.

Extract guidelines that cover:
- Betting strategies (when to bet, check, raise, fold)
- Position play (early, middle, late position)
- Board texture analysis (wet/dry, dynamic/static)
- Hand strength evaluation
- Bluffing opportunities
- Value betting spots
- Multi-way pot strategies
- Bankroll management
- Player exploitation

For each guideline, provide:
- A clear, actionable rule
- The situation/context where it applies
- The reasoning behind the strategy

Return ONLY valid JSON in this exact format:
[
  {{
    "title": "Brief title of the guideline",
    "category": "betting|position|board_texture|hand_strength|bluffing|value|multiway|bankroll|exploitation",
    "situation": "Specific situation where this applies",
    "action": "What to do in this situation",
    "reasoning": "Why this strategy works",
    "example": "Brief example if applicable"
  }}
]

Transcript chunk:
{transcript_chunk}
"""

def call_openai(prompt: str) -> str:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except ImportError:
        print("OpenAI library not installed. Install with: pip install openai")
        return None
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def call_anthropic(prompt: str) -> str:
    """Call Anthropic API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except ImportError:
        print("Anthropic library not installed. Install with: pip install anthropic")
        return None
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return None

def call_local_llm(prompt: str) -> str:
    """Call a local LLM (placeholder for Ollama, etc.)."""
    # This is a placeholder - you would implement your local LLM call here
    print("Local LLM not implemented. Please use OpenAI or Anthropic.")
    return None

def extract_guidelines_with_llm(transcript_chunk: str) -> List[Dict[str, Any]]:
    """Extract guidelines using the configured LLM."""
    prompt = create_guideline_prompt(transcript_chunk)
    
    if LLM_PROVIDER == "openai":
        response = call_openai(prompt)
    elif LLM_PROVIDER == "anthropic":
        response = call_anthropic(prompt)
    elif LLM_PROVIDER == "local":
        response = call_local_llm(prompt)
    else:
        print(f"Unknown LLM provider: {LLM_PROVIDER}")
        return []
    
    if not response:
        return []
    
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            guidelines = json.loads(json_match.group())
            return guidelines
        else:
            # If no JSON array found, try to parse the entire response
            guidelines = json.loads(response)
            return guidelines if isinstance(guidelines, list) else []
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response was: {response[:200]}...")
        return []

def process_transcripts():
    """Process all fixed transcripts and extract guidelines."""
    all_guidelines = []
    
    if not FIXED_DIR.exists():
        print(f"Fixed transcripts directory not found: {FIXED_DIR}")
        return
    
    transcript_files = list(FIXED_DIR.glob("*.txt"))
    print(f"Found {len(transcript_files)} transcript files")
    
    for i, file_path in enumerate(transcript_files, 1):
        print(f"\nProcessing {i}/{len(transcript_files)}: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if file is too short
            if len(content.strip()) < 100:
                print(f"  Skipping {file_path.name} (too short)")
                continue
            
            chunks = chunk_text(content)
            print(f"  Split into {len(chunks)} chunks")
            
            for chunk_idx, chunk in enumerate(chunks):
                print(f"  Processing chunk {chunk_idx + 1}/{len(chunks)}")
                guidelines = extract_guidelines_with_llm(chunk)
                
                # Add metadata to each guideline
                for guideline in guidelines:
                    guideline["source_file"] = file_path.name
                    guideline["chunk_id"] = chunk_idx
                    guideline["source_type"] = "transcript"
                
                all_guidelines.extend(guidelines)
                print(f"    Extracted {len(guidelines)} guidelines")
                
        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
    
    return all_guidelines

def save_guidelines(guidelines: List[Dict[str, Any]]):
    """Save guidelines to JSON file."""
    # Create output directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Add metadata
    output_data = {
        "metadata": {
            "total_guidelines": len(guidelines),
            "source_directory": str(FIXED_DIR),
            "llm_provider": LLM_PROVIDER,
            "chunk_size": CHUNK_SIZE,
            "overlap": OVERLAP
        },
        "guidelines": guidelines
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(guidelines)} guidelines to {OUTPUT_FILE}")

def main():
    """Main function."""
    print("Poker Transcript to Guidelines Converter")
    print("=" * 40)
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"Input Directory: {FIXED_DIR}")
    print(f"Output File: {OUTPUT_FILE}")
    print()
    
    # Check API keys
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return
    
    if LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Process transcripts
    guidelines = process_transcripts()
    
    if guidelines:
        save_guidelines(guidelines)
        
        # Print summary by category
        categories = {}
        for guideline in guidelines:
            cat = guideline.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nGuidelines by category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
    else:
        print("❌ No guidelines extracted")

if __name__ == "__main__":
    main()