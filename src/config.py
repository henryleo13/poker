import os
from src.models.config import ModelConfig

# Provider configuration examples
PROVIDER_CONFIGS = {
    "openai": ModelConfig(
        model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo"
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=6000  # Safe limit for GPT-4o Mini (8192 max)
    ),
    
    "claude-3": ModelConfig(
        #model="claude-3-sonnet-20240229",  # or "claude-3-opus-20240229"
        model="claude-3-haiku-20240307",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=3000  # Safe limit for Claude Haiku (4096 max
    ),

    "claude-4": ModelConfig(
        model="claude-sonnet-4-20250514",  # or "claude-4-100k
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=8000  # Safe limit for Claude 4 (128k max)
    ),
    
    "gemini": ModelConfig(
        model="gemini-pro",
        api_key=os.getenv("GOOGLE_API_KEY"),
        max_tokens=6000  # Safe limit for Gemini Pro (8192 max)
    ),
    
    "ollama": ModelConfig(
        model="ollama/llama2",  # Local model
        api_base="http://localhost:11434",
        max_tokens=6000  # Adjust based on your local model capabilities
    ),
    
    "azure": ModelConfig(
        model="azure/gpt-4",
        api_key=os.getenv("AZURE_API_KEY"),
        api_base=os.getenv("AZURE_API_BASE"),
        max_tokens=6000  # Adjust based on your Azure model capabilities
    )
}

def check_environment():
    """Check which API keys are available in environment variables"""
    required_vars = {
        'OpenAI': 'OPENAI_API_KEY',
        'Anthropic': 'ANTHROPIC_API_KEY', 
        'Google': 'GOOGLE_API_KEY',
        'Azure': 'AZURE_API_KEY'
    }
    
    print('🔍 Checking environment variables:')
    for provider, env_var in required_vars.items():
        is_set = bool(os.getenv(env_var))
        status = '✅' if is_set else '❌'
        print(f"  {provider}: {status} {env_var}")
