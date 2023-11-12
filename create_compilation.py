from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize

from pathlib import Path
import os
from os.path import isfile, join, exists
import random
import shutil 
from collections import defaultdict
import yaml 
import re
import datetime

num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
} 

VideoFileClip.resize = resize
compilation_output_path = ''
def extractAcc(filepath):
    try:
        filename = os.path.basename(filepath)
        tokens = filename.split("+")
        acc = tokens[0]
        return acc
    except:
        return ""

# generateTimeRange converts float seconds to a range of form @MM:SS
def generateTimeRange(duration, clipDuration):
    preHour = int(duration / 60)
    preMin = int(duration % 60)
    preTime = str(preHour // 10) + str(preHour % 10) + ":" + str(preMin // 10) + str(preMin % 10)

    duration += clipDuration
    postHour = int(duration / 60)
    postMin = int(duration % 60)
    postTime = str(postHour // 10) + str(postHour % 10) + ":" + str(postMin // 10) + str(postMin % 10)
    #return "@" + preTime + " - " + "@" + postTime
    return "@" + preTime

def makeCompilation(output_path, input_path):
    introName = "PathToIntroVideoClipMp4"
    outroName = 'PathToOutroVideoClipMp4'
    totalVidLength = 10*60
    minClipLength = 5
    maxClipLength = 80
    now = datetime.datetime.now()
    filename = num_to_month[now.month].upper() + "_" + str(now.year) + "_" + str(now.day) + ".mp4"
    outputFilePath = os.path.join(output_path, filename)
    allVideos = []
    seenLengths = defaultdict(list)
    totalLength = 0
    for fileName in os.listdir(input_path):
        filePath = join(input_path, fileName);
        if isfile(filePath) and fileName.endswith(".mp4"):
            # if os.stat(filePath).st_size < 5000:
            #     continue
            # else:
            #     print(f'{fileName} st_size = {os.stat(filePath).st_size}')
            #     print(f'st_size > 5000..skipping {filePath}')
            # print(f'{fileName} st_size = {os.stat(filePath).st_size} bytes')
            # Destination path  
            clip = VideoFileClip(filePath)
            clip = clip.resize(width=1920)
            clip = clip.resize(height=1080)
            duration = clip.duration
            # print(f'duration {duration}')
            if duration <= maxClipLength and duration >= minClipLength:
                allVideos.append(clip)
                seenLengths[duration].append(fileName)
                totalLength += duration

    print("Total Duration: " + str(totalLength))

    random.shuffle(allVideos)

    duration = 0
    # Add intro vid
    videos = []
    if introName != '':
        introVid = VideoFileClip("./" + introName)
        videos.append(introVid)
        duration += introVid.duration
    
    description = ""
    # Create videos
    for clip in allVideos:
        timeRange = generateTimeRange(duration, clip.duration)
        acc = extractAcc(clip.filename)
        description += timeRange + " : @" + acc + "\n"
        duration += clip.duration 
        videos.append(clip)
        print(duration)
        if duration >= totalVidLength:
            # Just make one video
            break
    
    # Add outro vid
    if outroName != 'outro_ vid.mp4':
        outroVid = VideoFileClip("./" + outroName)
        videos.append(outroVid)

    finalClip = concatenate_videoclips(videos, method="compose")

    if exists(outputFilePath):
        head_tail = os.path.split(outputFilePath)
        print('A compilation with that name already exists. Renaming...')
        count = ''
        for file in os.listdir('./'):
            if re.search(f"{head_tail[1]}.mp4", file):
                count += '_Copy'
        outputFilePath = os.path.join(head_tail[0], f'{count}.mp4')
    compilation_output_path = outputFilePath
    print(f'Writing compilation to {outputFilePath}')
    # Create compilation
    finalClip.write_videofile(outputFilePath, threads=16, remove_temp=True, codec="libx264", audio_codec="aac")

    return description

if __name__ == '__main__':
    now = datetime.datetime.now()
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    all_videos_path = os.path.join(config['INPUT_VIDEOS_PATH'], str(now.year), str(now.month), str(now.day))
    if not os.path.exists(all_videos_path):
        path = Path(all_videos_path)
        path.mkdir(parents=True)
    # Group all videos into one folder
    staging_dir = Path.cwd() / 'staging_folder'
    for file in list(staging_dir.rglob("*.mp4*")):
        if os.path.isfile(file):
            shutil.move(file, all_videos_path)
    makeCompilation(config['COMPILATION_OUTPUT_PATH'], all_videos_path)
    

# if __name__ == '__main__':
    
#     with open('config.yaml', 'r') as file:
#         config = yaml.safe_load(file)
#     if not os.path.exists(config['INPUT_VIDEOS_PATH']):
#         os.mkdir(config['INPUT_VIDEOS_PATH'])
#     INPUT_DIR = Path.cwd() / 'account_videos'
#     for file in list(INPUT_DIR.rglob("*.mp4*")):
#         shutil.move(file, config['INPUT_VIDEOS_PATH'])
#     makeCompilation(config['OUTPUT_PATH'], config['INPUT_VIDEOS_PATH'])
    
