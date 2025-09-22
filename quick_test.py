import asyncio
import os
from src.poker_processor import PokerTutorialProcessor
from src.config import PROVIDER_CONFIGS, check_environment

async def test():
    print("🔧 Testing LiteLLM connection...")
    
    # Check environment
    check_environment()
    
    # Test with your provider
    config = PROVIDER_CONFIGS["claude-3"]  # Change if using different provider
    
    if not config.api_key:
        print("❌ No API key found. Set environment variable:")
        print("   set OPENAI_API_KEY=your_key_here")
        return
    
    processor = PokerTutorialProcessor(config)
    
    connected = await processor.test_connection()
    if connected:
        print("✅ Connection successful! Ready to process transcripts!")
        print("Run: python main.py")
    else:
        print("❌ Connection failed - check your API key and internet connection")

if __name__ == "__main__":
    asyncio.run(test())