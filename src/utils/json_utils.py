import json
import re
from typing import Dict, Any

def clean_json_string(json_str: str) -> str:
    """Clean up LLM-generated JSON string to fix common issues"""
    # Remove markdown code blocks
    if json_str.strip().startswith("```json"):
        json_str = json_str.strip()[7:]
    if json_str.strip().endswith("```"):
        json_str = json_str.strip()[:-3]
    
    # Remove any leading/trailing whitespace
    json_str = json_str.strip()
    
    # Fix common control character issues
    # Replace problematic characters in string values only
    def fix_string_content(match):
        content = match.group(1)
        # Fix common control characters
        content = content.replace('\n', '\\n')
        content = content.replace('\r', '\\r')
        content = content.replace('\t', '\\t')
        content = content.replace('\b', '\\b')
        content = content.replace('\f', '\\f')
        # Fix unescaped quotes
        content = content.replace('"', '\\"')
        return f'"{content}"'
    
    # Apply fixes to content within quotes
    # This regex finds content between quotes that isn't already escaped
    json_str = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"', fix_string_content, json_str)
    
    return json_str

def parse_json_response(response: str, context: str = "") -> Dict[str, Any]:
    """Parse JSON response with error handling and cleanup"""
    try:
        # First attempt - try parsing as-is
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        return json.loads(cleaned_response)
        
    except json.JSONDecodeError as e:
        print(f"First parse attempt failed for {context}: {e}")
        print("Attempting to clean JSON...")
        
        try:
            # Second attempt - clean the JSON string
            cleaned_json = clean_json_string(response)
            return json.loads(cleaned_json)
            
        except json.JSONDecodeError as e2:
            print(f"Second parse attempt failed for {context}: {e2}")
            print("Attempting regex extraction...")
            
            try:
                # Third attempt - extract JSON from response using regex
                json_pattern = r'\{.*\}'
                matches = re.findall(json_pattern, response, re.DOTALL)
                
                if matches:
                    # Try the largest JSON object found
                    largest_match = max(matches, key=len)
                    cleaned_match = clean_json_string(largest_match)
                    return json.loads(cleaned_match)
                else:
                    raise Exception("No JSON object found in response")
                    
            except (json.JSONDecodeError, Exception) as e3:
                print(f"All JSON parsing attempts failed for {context}")
                print(f"Original error: {e}")
                print(f"Cleaned JSON error: {e2}")
                print(f"Regex extraction error: {e3}")
                print(f"Raw response (first 500 chars): {response[:500]}")
                
                # Last resort - try to salvage what we can
                if context == "chunking":
                    return {"chunks": []}
                elif context == "questions":
                    return {"questions": []}
                elif context == "rules":
                    return {
                        "bet_sizing_rules": [],
                        "flop_guidelines": [],
                        "turn_guidelines": [],
                        "river_guidelines": [],
                        "general_principles": []
                    }
                else:
                    raise Exception(f"Failed to parse JSON response {context}: {e}")