import asyncio
import json
from pathlib import Path
from src.poker_processor import PokerTutorialProcessor
from src.config import PROVIDER_CONFIGS, check_environment

async def main():
    """
    Main execution function
    """
    # Check environment setup
    check_environment()
    
    # Choose your provider configuration
    config = PROVIDER_CONFIGS["claude-3"]  # Change this to your preferred provider
    
    processor = PokerTutorialProcessor(config)
    
    # Test connection first
    connected = await processor.test_connection()
    if not connected:
        print("Failed to connect to LLM provider. Please check your configuration.")
        return
    
    # Process a single transcript (uncomment to use)
    await processor.process_transcript(Path("./guides/fixed_transcripts/3. You're Sizing Bets Wrong.txt"))
    
    # Process all transcripts in a directory
    #await processor.process_all_transcripts(Path("./guides/fixed_transcripts"))
    
    # Get and display processing statistics
    stats = processor.get_stats()
    print('\n📊 Processing Statistics:')
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())