import os
from pathlib import Path
import yaml

if __name__ == '__main__':
    if not os.path.exists("./config.yaml"):
        raise 'No config.yaml file found'

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Create account_videos directory if not exists
    if not os.path.exists("./staging_folder"):
        os.makedirs("./staging_folder")

    # Login to instagram on the firefox web browser

    # Harvest instagram cookies from firefox
    os.system("import_cookies.py")

    # Login using instaloader
    os.system('login.bat')

    # Scrape videos from instagram followers
    os.system('insta_video_scraper.bat')

    # Create a compilation from downloaded videos
    os.system('create_compilation.py')

    # Upload to Youtube
    os.system('upload_ytvid.py')

