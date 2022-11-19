import os
import json
import subprocess
from ast import literal_eval

def create_path(filepath):
    if not os.path.exists(filepath):
        try:
            os.makedirs(filepath)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

likes_path = "likes"

create_path(likes_path)

tweetIds = []
for file in os.listdir(likes_path):
    tweetIds.append(os.path.splitext(file)[0])

with open("like.js", "r", encoding="utf-8") as f:
    data = f.read()

data = literal_eval(data[data.find("["):])
for i, tweet in enumerate(data):
    tweetId = tweet["like"]["tweetId"]
    if tweetId in tweetIds:
        continue

    try:
        output = json.loads(subprocess.check_output(["snscrape", "--jsonl", "twitter-tweet", tweetId], creationflags = 0x08000000))
        print(f"Stored: {tweetId} ({i+1}/{len(data)})")
        output_path = os.path.join(likes_path, f"{tweetId}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(output, indent='\t', separators=(',', ': ')))
    except:
        pass
