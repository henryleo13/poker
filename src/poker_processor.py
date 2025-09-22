import os
import asyncio
from pathlib import Path
from typing import Dict, Any
from src.models.config import ModelConfig
from src.utils.llm_client import LLMClient
from src.utils.file_utils import ensure_directory_exists, initialize_json_file, load_json
from src.processing_agents import ChunkingAgent, QuestionAgent, RulesAgent

class PokerTutorialProcessor:
    """
    Main orchestrator for the sequential agent system that processes poker tutorial transcripts.
    
    Coordinates three specialized agents:
    - ChunkingAgent: Breaks transcripts into logical sections
    - QuestionAgent: Generates test questions from chunks
    - RulesAgent: Extracts actionable rules and guidelines
    """
    
    def __init__(self, config: ModelConfig = None):
        self.config = config or ModelConfig()
        self.output_dir = Path("./poker_output")
        self.questions_file = self.output_dir / "questions.json"
        self.rules_file = self.output_dir / "poker_rules.json"
        
        # Initialize output directory and files
        self._initialize_output_dir()
        
        # Set up LiteLLM client and agents
        self._setup_clients_and_agents()
        
        # Set up API key environment variable
        if self.config.api_key:
            os.environ[self._get_api_key_env_var()] = self.config.api_key
    
    def _get_api_key_env_var(self) -> str:
        """Get the appropriate environment variable name for the model's API key"""
        model_lower = self.config.model.lower()
        if "gpt" in model_lower or "openai" in model_lower:
            return "OPENAI_API_KEY"
        elif "claude" in model_lower or "anthropic" in model_lower:
            return "ANTHROPIC_API_KEY"
        elif "gemini" in model_lower or "google" in model_lower:
            return "GOOGLE_API_KEY"
        elif "azure" in model_lower:
            return "AZURE_API_KEY"
        else:
            return "API_KEY"
    
    def _initialize_output_dir(self):
        """Create output directory and initialize JSON files if they don't exist"""
        ensure_directory_exists(self.output_dir)
        
        # Initialize questions file
        initialize_json_file(self.questions_file, [])
        
        # Initialize rules file
        initial_rules = {
            "bet_sizing_rules": [],
            "flop_guidelines": [],
            "turn_guidelines": [],
            "river_guidelines": [],
            "general_principles": []
        }
        initialize_json_file(self.rules_file, initial_rules)
    
    def _setup_clients_and_agents(self):
        """Initialize LLM client and specialized agents"""
        self.llm_client = LLMClient(self.config)
        self.chunking_agent = ChunkingAgent(self.llm_client, self.output_dir)
        self.question_agent = QuestionAgent(self.llm_client, self.output_dir)
        self.rules_agent = RulesAgent(self.llm_client, self.output_dir)
    
    async def process_transcript(self, transcript_path: Path):
        """
        Main processing pipeline: runs all three agents sequentially
        
        Args:
            transcript_path: Path to the transcript file to process
        """
        try:
            print(f"\n🚀 Processing {transcript_path.name}...")
            transcript_name = transcript_path.stem
            
            # Agent 1: Chunk the transcript
            print("📝 Agent 1: Chunking transcript...")
            chunks = await self.chunking_agent.process(transcript_path)
            
            # Agent 2: Generate questions
            print("❓ Agent 2: Generating questions...")
            await self.question_agent.process(chunks, transcript_name)
            
            # Agent 3: Extract rules
            print("📋 Agent 3: Extracting rules...")
            await self.rules_agent.process(chunks, transcript_name)
            
            print(f"✅ Successfully processed {transcript_name}")
            
        except Exception as e:
            print(f"Error processing transcript {transcript_path}: {e}")
    
    async def process_all_transcripts(self, transcripts_dir: Path):
        """
        Process all .txt files in the specified directory
        
        Args:
            transcripts_dir: Directory containing transcript files
        """
        try:
            transcripts_dir = Path(transcripts_dir)
            txt_files = list(transcripts_dir.glob("*.txt"))
            
            print(f"Found {len(txt_files)} transcript files to process")
            
            for file_path in txt_files:
                await self.process_transcript(file_path)
                
                # Small delay to avoid rate limiting
                print("⏳ Waiting 2 seconds to avoid rate limits...")
                await asyncio.sleep(2)
            
            print("\n🎉 All transcripts processed successfully!")
            
        except Exception as e:
            print(f"Error processing transcripts: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics from generated files
        
        Returns:
            Dictionary containing comprehensive statistics
        """
        try:
            questions = load_json(self.questions_file)
            rules = load_json(self.rules_file)
            
            stats = {
                "total_questions": len(questions),
                "questions_by_street": {},
                "questions_by_difficulty": {},
                "questions_by_type": {},
                "total_rules": len(rules["bet_sizing_rules"]),
                "total_guidelines": {
                    "flop": len(rules["flop_guidelines"]),
                    "turn": len(rules["turn_guidelines"]),
                    "river": len(rules["river_guidelines"])
                },
                "general_principles": len(rules["general_principles"])
            }
            
            # Count questions by various categories
            for question in questions:
                street = question.get("street", "unknown")
                difficulty = question.get("difficulty", "unknown")
                q_type = question.get("question_type", "unknown")
                
                stats["questions_by_street"][street] = stats["questions_by_street"].get(street, 0) + 1
                stats["questions_by_difficulty"][difficulty] = stats["questions_by_difficulty"].get(difficulty, 0) + 1
                stats["questions_by_type"][q_type] = stats["questions_by_type"].get(q_type, 0) + 1
            
            return stats
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
    
    async def test_connection(self) -> bool:
        """
        Test LiteLLM connection and model availability
        
        Returns:
            True if connection successful, False otherwise
        """
        return await self.llm_client.test_connection()