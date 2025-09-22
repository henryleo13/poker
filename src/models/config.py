from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelConfig:
    """Configuration for LiteLLM model settings"""
    model: str = "gpt-4o-mini" # default model
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 3000  # Safe for most models including Claude Haiku (4096 max)
    timeout: int = 60