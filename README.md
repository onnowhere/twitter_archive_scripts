# Twitter Archive Scripts
Quick scripts made to assist in archiving twitter data

- `get_like_data.py`
    - Requires snscrape to be pip installed: https://github.com/JustAnotherArchivist/snscrape
    - Download an archive of your twitter data, then extract the `like.js` file into a folder with this script
    - Run the script to get a separate json metadata file for each liked tweet in the `likes` folder
- `get_like_media.py`
    - Downloads all media files from the output of `get_like_data.py`
    - Run the script to download all media files in a tweet (images, videos, gifs) to `likes_media` and profile pictures and banners to `likes_profile_media`
