import json
import random
import os

# -----------------------------
# Load guidelines from JSON file
# -----------------------------
def load_guidelines(filename="poker_guidelines.json"):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found. Save your guideline JSON first.")
    with open(filename, "r") as f:
        return json.load(f)

# -----------------------------
# Extract all practice questions
# -----------------------------
def extract_questions(guidelines):
    questions = []

    def recurse(node, path=""):
        if isinstance(node, dict):
            for key, value in node.items():
                recurse(value, path + "/" + key)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                recurse(item, path + f"/[{i}]")
        else:
            if path.endswith("guideline"):
                # path example: /multiway/sizing/comp_play_for_stacks_hand/guideline
                q_path = path.split("/")
                topic = q_path[1] if len(q_path) > 1 else "general"
                questions.append({
                    "topic": topic,
                    "question": node,
                    "path": path
                })

    recurse(guidelines)
    return questions

# -----------------------------
# Quiz loop
# -----------------------------
def run_quiz(questions, guidelines):
    print("=== Poker Trainer (Multiway Spot Practice) ===")
    print("Type 'exit' anytime to quit.\n")

    while True:
        q = random.choice(questions)
        print(f"\nTopic: {q['topic'].capitalize()}")
        print(f"Scenario: {q['question']}")
        user_input = input("Your action/thought? ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting trainer. Good luck at the tables!")
            break

        # Reveal answer by walking back to the full entry in JSON
        path_parts = q["path"].strip("/").split("/")
        node = guidelines
        for p in path_parts[:-1]:  # walk until parent
            node = node[p]

        # Show additional reasoning if exists
        print("\n--- Guideline ---")
        print(f"Recommended: {node.get('guideline', q['question'])}")
        if "reason" in node:
            print(f"Reason: {node['reason']}")
        if "example" in node:
            print(f"Example: {node['example']}")
        print("-----------------\n")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    guidelines = load_guidelines("poker_guidelines.json")
    questions = extract_questions(guidelines)
    run_quiz(questions, guidelines)
