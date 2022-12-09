# Twitter Archive Scripts
Quick scripts made to assist in archiving twitter data

## Liked Tweets
Twitter's user data archive does not contain metadata or media from liked tweets. These scripts help to gather data from liked tweets.

- `get_like_data.py`
    - Requires `snscrape` (https://github.com/JustAnotherArchivist/snscrape) and `ujson` (https://github.com/ultrajson/ultrajson) to be `pip install`ed
    - Request and download an archive of your Twitter data: https://twitter.com/settings/download_your_data
    - Extract the `like.js` file into a folder with this script
    - Run the script to get a separate json metadata file for each liked tweet in the `likes` folder
- `get_like_media.py`
    - Run `get_like_data.py` before running this script
    - Run the script to download all media files (images, videos, gifs) in your liked tweets to `likes_media` and profile pictures and banners to `likes_profile_media`
