# Create a simple test file: test_connection.py
import asyncio
from src.poker_processor import PokerTutorialProcessor
from src.config import PROVIDER_CONFIGS, check_environment

async def test():
    check_environment()
    config = PROVIDER_CONFIGS["openai"]
    processor = PokerTutorialProcessor(config)
    
    connected = await processor.test_connection()
    if connected:
        print("✅ Ready to process transcripts!")
    else:
        print("❌ Connection failed - check your API key")

asyncio.run(test())