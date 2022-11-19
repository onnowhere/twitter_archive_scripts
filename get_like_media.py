import os
import json
import shutil
import requests
import mimetypes
import subprocess
from ast import literal_eval
from urllib.parse import urlparse
from urllib.parse import parse_qs

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_path(filepath):
    if not os.path.exists(filepath):
        try:
            os.makedirs(filepath)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def download_media(url, file_path, get_extension=False):
    r = requests.get(url, stream=True, verify=False)

    if get_extension:
        content_type = r.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        file_path = f"{file_path}{ext}"
    
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

def get_url_file_name(url):
    return urlparse(url).path.rsplit("/", 1)[-1]

likes_path = "likes"
likes_media_path = "likes_media"
profile_media_path = "likes_profile_media"

create_path(likes_path)
create_path(likes_media_path)
create_path(profile_media_path)

likes_media_files = []
for file in os.listdir(likes_media_path):
    likes_media_files.append(os.path.splitext(file)[0])

profile_media_files = []
for file in os.listdir(profile_media_path):
    profile_media_files.append(os.path.splitext(file)[0])

tweet_count = len(os.listdir(likes_path))
for i, file in enumerate(os.listdir(likes_path)):
    tweetId = os.path.splitext(file)[0]
    file_path = os.path.join(likes_path, file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.loads(f.read())

    if "media" not in content.keys() or content["media"] is None:
        continue

    for media in content["media"]:
        url = None
        file_name = None
        get_extension = False
        if media["_type"] == "snscrape.modules.twitter.Photo":
            url = media["fullUrl"]
            file_name = get_url_file_name(url)
            get_extension = True
        elif media["_type"] == "snscrape.modules.twitter.Video":
            url = max(media["variants"], key=lambda x: int(x["bitrate"] or 0))["url"]
            file_name = get_url_file_name(url)
        else:
            url = max(media["variants"], key=lambda x: int(x["bitrate"] or 0))["url"]
            file_name = get_url_file_name(url)

        if url is not None and file_name is not None:
            file_name = f"{tweetId}-{file_name}"
            file_path = os.path.join(likes_media_path, file_name)
            if os.path.splitext(file_name)[0] not in likes_media_files:
                try:
                    print(f"Downloading: {file_name} (Tweet {i + 1}/{tweet_count})")
                    download_media(url, file_path, get_extension)
                except:
                    print(f"Failed to download: {url}")
                    pass

    profile_urls = []

    user = content.get("user")
    if user is not None:
        profile_image_url = user.get("profileImageUrl")
        if profile_image_url is not None:
            profile_urls.append(profile_image_url.replace("_normal", ""))

        profile_banner_url = user.get("profileBannerUrl")
        if profile_banner_url is not None:
            profile_urls.append(profile_banner_url)

    for url in profile_urls:
        profile_id = content["user"]["id"]
        name = get_url_file_name(url)
        file_name = f"{profile_id}-{name}"
        file_path = os.path.join(profile_media_path, file_name)
        get_extension = os.path.splitext(file_name)[1] == ""
        if os.path.splitext(file_name)[0] not in profile_media_files:
            try:
                print(f"Downloading: {file_name} (Tweet {i + 1}/{tweet_count})")
                download_media(url, file_path, get_extension)
            except:
                print(f"Failed to download: {url}")
                pass
