import json

with open('seed_tasks_5MB.jsonl', 'r') as file:
    for i, line in enumerate(file, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error in line {i}: {e}")
