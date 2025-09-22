import json
from pathlib import Path
from typing import Dict, Any, List

def ensure_directory_exists(path: Path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)

def initialize_json_file(file_path: Path, initial_data: Any):
    """Initialize JSON file with initial data if it doesn't exist"""
    if not file_path.exists():
        with open(file_path, 'w') as f:
            json.dump(initial_data, f, indent=2)

def load_json(file_path: Path) -> Any:
    """Load JSON data from file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path: Path, data: Any):
    """Save data to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def append_to_json_list(file_path: Path, new_items: List[Any]):
    """Append items to a JSON list file"""
    existing_data = load_json(file_path)
    existing_data.extend(new_items)
    save_json(file_path, existing_data)