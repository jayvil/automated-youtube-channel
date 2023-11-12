import datetime
from googleapiclient.http import MediaFileUpload
import shutil
import yaml
from create_compilation import compilation_output_path

def uploadYtvid(VIDEO_FILE_NAME='',
                title='Intro Video!',
                description=':) ',
                tags=[],
                googleAPI=None):
    
    now = datetime.datetime.now()
    upload_date_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, int(now.second)).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': 23
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)

    response_upload = googleAPI.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    """
    googleAPI.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload('thumbnail.png')
    ).execute()
    """

    
    return 1

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    user = 'Insert Username'
    uploadYtvid(VIDEO_FILE_NAME=f'PathToCompilationMp4')
    