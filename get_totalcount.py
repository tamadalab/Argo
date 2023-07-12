import os
import json
import sys

def get_total_count(filepath):
    # Open the JSON file
    with open(filepath) as f:
        data = json.load(f)
        if 'data' in data and 'repository' in data['data'] and 'issues' in data['data']['repository']:
            return data['data']['repository']['issues']['totalCount']
    return 0

# Use command line arguments for directories
path_parts = sys.argv[1:]

base_dir = "cache"
total_counts = {}

for part in path_parts:
    directory = os.path.join(base_dir, part, "issues", "json", "1.json")
    total_count = get_total_count(directory)
    total_counts[directory] = total_count
    print(f"Total count for {directory} : {total_count}")

print(f"Overall total count: {sum(total_counts.values())}")
