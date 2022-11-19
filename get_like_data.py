import os
import ujson
import json
import subprocess
import time
import traceback
import snscrape.modules.twitter as sntwitter

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
    print("Reading like.js")
    data = f.read()

print("Evaluating like.js as JSON")
likes = ujson.loads(data[data.find("["):])
print(f"Found {len(likes)} liked tweets")

print("Scraping tweets")
for i, tweet in enumerate(likes):
    tweetId = tweet["like"]["tweetId"]
    if tweetId in tweetIds:
        continue

    try:
        print(f"Scraping tweet {tweetId}")
        tweetScraper = sntwitter.TwitterTweetScraper(tweetId)
        tweetData = next(tweetScraper.get_items())
        output = tweetData.json()

        output_path = os.path.join(likes_path, f"{tweetId}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(output, indent='\t', separators=(',', ': ')))

        print(f"Stored tweet {tweetId} ({i + 1}/{len(likes)})")
    except Exception:
        print(f"Could not store tweet at https://twitter.com/i/web/status/{tweetId} (user may be private)")
        # traceback.print_exc()
