"""
Combined agents for poker tutorial processing.
All three agents (Chunking, Question Generation, Rules Extraction) in one file.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
from src.utils.llm_client import LLMClient
from src.utils.json_utils import parse_json_response
from src.utils.file_utils import load_json, save_json
from src.prompts import (
    chunking_prompt,
    question_generation_prompt,
    rules_extraction_prompt
)

class BaseAgent(ABC):
    """Base class for all processing agents"""
    
    def __init__(self, llm_client: LLMClient, output_dir: Path):
        self.llm_client = llm_client
        self.output_dir = output_dir
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Any:
        """Main processing method to be implemented by each agent"""
        pass
    
    async def _call_llm_and_parse(self, prompt: str, context: str, **kwargs) -> Dict[str, Any]:
        """Helper method to call LLM and parse JSON response"""
        # Use config max_tokens as default, but allow override
        if 'max_tokens' not in kwargs:
            kwargs['max_tokens'] = self.llm_client.config.max_tokens
        
        response = await self.llm_client.call(prompt, **kwargs)
        return parse_json_response(response, context)

class ChunkingAgent(BaseAgent):
    """Agent 1: Break transcript into logical, coherent chunks"""
    
    async def process(self, transcript_path: Path) -> Dict[str, Any]:
        """
        Chunk a transcript into logical sections
        
        Args:
            transcript_path: Path to the transcript file
            
        Returns:
            Dictionary containing chunks with metadata
        """
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()
            
            # Get prompt from prompts module
            prompt = chunking_prompt(transcript)
            
            chunks = await self._call_llm_and_parse(prompt, "chunking")
            
            # Save chunks to file
            chunks_file = self.output_dir / f"chunks_{transcript_path.stem}.json"
            with open(chunks_file, 'w') as f:
                json.dump(chunks, f, indent=2)
            
            print(f"✅ Chunked {transcript_path.name} into {len(chunks['chunks'])} chunks")
            return chunks
            
        except Exception as e:
            print(f"Error chunking transcript {transcript_path}: {e}")
            raise

class QuestionAgent(BaseAgent):
    """Agent 2: Generate specific, testable questions from chunks"""
    
    def __init__(self, llm_client: LLMClient, output_dir: Path):
        super().__init__(llm_client, output_dir)
        self.questions_file = output_dir / "questions.json"
    
    async def process(self, chunks: Dict[str, Any], transcript_name: str) -> List[Dict[str, Any]]:
        """
        Generate test questions from transcript chunks
        
        Args:
            chunks: Dictionary containing transcript chunks
            transcript_name: Name of the source transcript
            
        Returns:
            List of generated questions
        """
        try:
            # Get prompt from prompts module
            prompt = question_generation_prompt(chunks, transcript_name)
            
            new_questions = await self._call_llm_and_parse(prompt, "questions")
            
            # Load existing questions and append new ones
            existing_questions = load_json(self.questions_file)
            existing_questions.extend(new_questions["questions"])
            save_json(self.questions_file, existing_questions)
            
            print(f"✅ Generated {len(new_questions['questions'])} questions from {transcript_name}")
            return new_questions["questions"]
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            raise

class RulesAgent(BaseAgent):
    """Agent 3: Extract actionable rules and guidelines from chunks"""
    
    def __init__(self, llm_client: LLMClient, output_dir: Path):
        super().__init__(llm_client, output_dir)
        self.rules_file = output_dir / "poker_rules.json"
    
    async def process(self, chunks: Dict[str, Any], transcript_name: str) -> Dict[str, Any]:
        """
        Extract actionable rules and guidelines from chunks
        
        Args:
            chunks: Dictionary containing transcript chunks
            transcript_name: Name of the source transcript
            
        Returns:
            Dictionary containing extracted rules by category
        """
        try:
            # Get prompt from prompts module
            prompt = rules_extraction_prompt(chunks, transcript_name)
            
            new_rules = await self._call_llm_and_parse(prompt, "rules")
            
            # Load existing rules and merge
            existing_rules = load_json(self.rules_file)
            
            # Merge each rule category
            for category in ["bet_sizing_rules", "flop_guidelines", "turn_guidelines", 
                           "river_guidelines", "general_principles"]:
                if category in new_rules:
                    existing_rules[category].extend(new_rules[category])
            
            save_json(self.rules_file, existing_rules)
            
            print(f"✅ Extracted rules from {transcript_name}")
            return new_rules
            
        except Exception as e:
            print(f"Error extracting rules: {e}")
            raise

# Export all agents for easy importing
__all__ = ['BaseAgent', 'ChunkingAgent', 'QuestionAgent', 'RulesAgent']