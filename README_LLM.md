# Poker Transcript to Guidelines Converter

This tool converts your cleaned poker transcripts into structured JSON guidelines using Large Language Models (LLMs).

## Features

- **Multiple LLM Support**: OpenAI GPT-4, Anthropic Claude, or local models
- **Intelligent Chunking**: Splits long transcripts into manageable pieces
- **Structured Output**: Extracts actionable poker guidelines in JSON format
- **Category Organization**: Automatically categorizes guidelines by type
- **Metadata Tracking**: Tracks source files and processing details

## Quick Start

### 1. Setup

```bash
# Install dependencies
python setup_llm.py

# Or manually install
pip install -r requirements.txt
```

### 2. Set API Key

Choose one LLM provider and set the API key:

**OpenAI (Recommended)**
```bash
# Windows
set OPENAI_API_KEY=your-openai-key-here

# Linux/Mac
export OPENAI_API_KEY=your-openai-key-here
```

**Anthropic Claude**
```bash
# Windows
set ANTHROPIC_API_KEY=your-anthropic-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-anthropic-key-here
```

### 3. Run the Converter

```bash
python create_json.py
```

## Configuration

Edit `create_json.py` to customize:

```python
# Choose LLM provider
LLM_PROVIDER = "openai"  # Options: "openai", "anthropic", "local"

# Adjust chunking
CHUNK_SIZE = 2000  # Characters per chunk
OVERLAP = 200      # Overlap between chunks
```

## Output Format

The script generates `guides/poker_guidelines.json` with this structure:

```json
{
  "metadata": {
    "total_guidelines": 150,
    "source_directory": "guides/fixed_transcripts",
    "llm_provider": "openai",
    "chunk_size": 2000,
    "overlap": 200
  },
  "guidelines": [
    {
      "title": "C-bet on dry ace-high boards",
      "category": "betting",
      "situation": "Heads up on dry ace-high flop",
      "action": "C-bet small with entire range",
      "reasoning": "Our range advantage is strong on ace-high boards",
      "example": "A72 rainbow - bet 1/3 pot with all hands",
      "source_file": "1. 95% of Pots are Multiway.txt",
      "chunk_id": 0,
      "source_type": "transcript"
    }
  ]
}
```

## Categories

Guidelines are automatically categorized into:

- **betting**: When to bet, check, raise, fold
- **position**: Early, middle, late position play
- **board_texture**: Wet/dry, dynamic/static boards
- **hand_strength**: Strong, weak, marginal hands
- **bluffing**: Bluffing opportunities and sizing
- **value**: Value betting spots and sizing
- **multiway**: Multi-way pot strategies
- **bankroll**: Bankroll management
- **exploitation**: Player-specific strategies

## Troubleshooting

### API Key Issues
- Make sure your API key is set correctly
- Check that you have credits/quota remaining
- Verify the key has the right permissions

### JSON Parsing Errors
- The LLM might return malformed JSON
- Check the console output for error details
- Try reducing CHUNK_SIZE if responses are too long

### Rate Limits
- Add delays between API calls if hitting rate limits
- Reduce CHUNK_SIZE to process faster
- Use a more powerful model for better results

## Cost Estimation

**OpenAI GPT-4o-mini** (recommended):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Estimated cost: $1-5 for all transcripts

**Anthropic Claude Haiku**:
- ~$0.25 per 1M input tokens  
- ~$1.25 per 1M output tokens
- Estimated cost: $2-8 for all transcripts

## Next Steps

After generating guidelines, you can:

1. **Review and filter** the guidelines for quality
2. **Import into your poker app** for reference
3. **Create flashcards** for study
4. **Build a search interface** for quick lookup
5. **Generate practice scenarios** based on the guidelines
