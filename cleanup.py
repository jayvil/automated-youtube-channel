import shutil
import os
import yaml
import time

if __name__ == '__main__':
    print("Cleanup...")
    if not os.path.exists("./config.yaml"):
        raise 'No config.yaml file found'

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    # Delete staging folder
    shutil.rmtree('./staging_folder')
    size = 0
    for path, dirs, files in os.walk(config['INPUT_VIDEOS_PATH']):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    
    # Remove oldest videos directory if folder size > 2Gb
    if size > 2**21.416413017506358: # 1gb = 1billion bytes 2^20.72326583694641 ~ 2gb
        numdays = 86400*7
        now = time.time()
        for path, dirs, files in os.walk(config['INPUT_VIDEOS_PATH']):
            for dir in path:
                timestamp = os.path.getmtime(os.path.join(path,dir))
                if now-numdays > timestamp:
                    try:
                        print("removing ",os.path.join(path,dir))
                        shutil.rmtree(os.path.join(path,dir))
                    except Exception as e:
                        print(e)
                        pass
                    else: 
                        print(f'Removed {os.path.join(path,dir)}')