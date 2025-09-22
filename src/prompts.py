"""
Centralized prompts for all poker processing agents.
Each prompt is a function that takes parameters and returns the formatted prompt string.
"""

import json
from typing import Dict, Any

def chunking_prompt(transcript: str) -> str:
    """Generate chunking prompt for Agent 1"""
    return f"""
You are a poker strategy expert. Analyze this poker tutorial transcript and break it into logical, coherent chunks.

Each chunk should:
1. Focus on a single concept or scenario
2. Be 1000-2000 words long (comprehensive coverage)
3. Include complete thoughts and examples
4. Have a clear topic/theme
5. Preserve strategic context and reasoning flow

IMPORTANT: Return ONLY a valid JSON object. Do not include any markdown formatting, explanations, or other text.

JSON Structure:
{{
  "chunks": [
    {{
      "id": 1,
      "topic": "Brief topic description",
      "content": "The actual chunk content - escape all quotes and newlines properly",
      "street": "preflop/flop/turn/river/general",
      "key_concepts": ["concept1", "concept2"],
      "word_count": 1200
    }}
  ]
}}

CRITICAL: 
- Escape all quotes in content with \"
- Replace actual newlines in content with \\n
- Do not use unescaped control characters
- Ensure all JSON values are properly quoted and escaped

Transcript:
{transcript}
"""

def question_generation_prompt(chunks: Dict[str, Any], transcript_name: str) -> str:
    """Generate question generation prompt for Agent 2"""
    return f"""
You are a poker coach creating practice questions. Based on these poker strategy chunks, generate specific, actionable test questions.

Create questions that test:
1. Decision-making in specific scenarios
2. Understanding of concepts
3. Application of sizing principles
4. Recognition of board textures and opponent tendencies

For each chunk, generate 2-4 questions based on the chunk's complexity and content. 

IMPORTANT: Return ONLY a valid JSON object. Do not include any markdown formatting, explanations, or other text.

JSON Structure:
{{
  "questions": [
    {{
      "id": "unique_id",
      "source_transcript": "{transcript_name}",
      "source_chunk_id": 1,
      "question_type": "scenario/concept/application",
      "street": "preflop/flop/turn/river",
      "question": "The actual question text - escape quotes properly",
      "scenario": {{
        "position": "BTN/SB/BB/UTG/etc or null",
        "stack_size": "effective stack in BBs or null",
        "board": "board cards if applicable or null",
        "action": "previous action sequence or null",
        "hero_hand": "if specified or example hand or null"
      }},
      "correct_answer": "detailed explanation of correct play - escape quotes properly",
      "key_concepts": ["concept1", "concept2"],
      "difficulty": "beginner/intermediate/advanced"
    }}
  ]
}}

CRITICAL: 
- Escape all quotes in text with \"
- Replace actual newlines with \\n
- Ensure all JSON values are properly quoted and escaped

Chunks to analyze:
{json.dumps(chunks, indent=2)}
"""

def rules_extraction_prompt(chunks: Dict[str, Any], transcript_name: str) -> str:
    """Generate rules extraction prompt for Agent 3"""
    return f"""
You are a poker strategist extracting actionable rules and guidelines from this tutorial.

Extract specific, implementable rules. 

IMPORTANT: Return ONLY a valid JSON object. Do not include any markdown formatting, explanations, or other text.

JSON Structure:
{{
  "bet_sizing_rules": [
    {{
      "rule_id": "unique_id",
      "source": "{transcript_name}",
      "condition": "when this situation occurs",
      "action": "do this specific action",
      "reasoning": "why this works",
      "street": "flop/turn/river/general",
      "priority": "high/medium/low",
      "examples": ["example1", "example2"]
    }}
  ],
  "flop_guidelines": [
    {{
      "guideline_id": "unique_id",
      "source": "{transcript_name}", 
      "board_type": "wet/dry/static/dynamic",
      "opponent_tendency": "fast_play/trap/capped/uncapped",
      "sizing_strategy": "specific strategy",
      "value_bluff_relationship": "same_size/different_sizes",
      "position_considerations": "position-specific notes"
    }}
  ],
  "turn_guidelines": [
    {{
      "guideline_id": "unique_id",
      "source": "{transcript_name}",
      "scenario": "scenario description",
      "key_question": "will opponent fast play?",
      "recommended_action": "specific action",
      "size_guideline": "sizing recommendation",
      "multiway_considerations": "adjustments for multiway pots"
    }}
  ],
  "river_guidelines": [
    {{
      "guideline_id": "unique_id", 
      "source": "{transcript_name}",
      "scenario_type": "bluff_big_value_small/bluff_small_value_big/etc",
      "opponent_range": "capped/uncapped/strong/weak",
      "sizing_strategy": "specific strategy",
      "stack_depth_factors": "deep vs shallow considerations"
    }}
  ],
  "general_principles": [
    {{
      "principle_id": "unique_id",
      "source": "{transcript_name}",
      "principle": "general principle statement",
      "application": "how to apply this",
      "exceptions": "when this doesn't apply"
    }}
  ]
}}

CRITICAL: 
- Escape all quotes in text with \"
- Replace actual newlines with \\n
- Ensure all JSON values are properly quoted and escaped

Focus on extracting:
- Specific bet sizing formulas
- Board texture recognition rules
- Opponent tendency classifications
- Street-specific strategies
- Position and stack depth considerations

Chunks to analyze:
{json.dumps(chunks, indent=2)}
"""

# Optional: Test prompts for development/debugging
def connection_test_prompt() -> str:
    """Simple test prompt for connection verification"""
    return "Respond with just the word 'connected' if you can read this."