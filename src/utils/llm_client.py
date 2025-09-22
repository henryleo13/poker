import asyncio
from typing import Dict, Any
from litellm import acompletion
from src.models.config import ModelConfig

class LLMClient:
    """Centralized LiteLLM client with retry logic and error handling"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
    
    async def call(self, prompt: str, **kwargs) -> str:
        """Make LiteLLM API call with retry logic"""
        max_retries = 3
        last_error = None
        
        call_params = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "timeout": self.config.timeout,
            **kwargs
        }
        
        if self.config.api_base:
            call_params["api_base"] = self.config.api_base
        
        for attempt in range(max_retries):
            try:
                response = await acompletion(**call_params)
                return response.choices[0].message.content
                
            except Exception as error:
                last_error = error
                print(f"LLM call attempt {attempt + 1} failed: {error}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
        
        raise Exception(f"All LLM call attempts failed. Last error: {last_error}")
    
    async def test_connection(self) -> bool:
        """Test LiteLLM connection and model availability"""
        try:
            from src.prompts import connection_test_prompt
            test_prompt = connection_test_prompt()
            response = await self.call(test_prompt, max_tokens=10)
            print(f"✅ LiteLLM connection test successful: {response.strip()}")
            return True
        except Exception as e:
            print(f"❌ LiteLLM connection test failed: {e}")
            return False