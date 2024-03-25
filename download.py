import requests
import logging
import json
import sys
import os
from lxml import etree
from website import WebClient




def reqncopy(s, req, headers, file, fullsize, Logs):
    resp = s.get(req, headers=headers, stream=True)
    i = 0
    for chunk in resp.iter_content(chunk_size=128):
        if i%81920 == 0:
            Logs.log(f"{i*128}/{fullsize}   ({round(i*128*100/fullsize, 2)}%)")
        file.write(chunk)
        i = i + 1
    return resp


def get_segments(s, vid):
    req=f"{vid[:-3]}mpd"
    resp = s.get(req)
    tree = etree.fromstring(resp.text)
    seglist = tree[1][0][2][2]
    segments = []
    for i in seglist:
        segments.append(i.values()[0])
    return segments


def gen_videodownload(rng):
    return {'Origin': 'https://ru.pastrycampus.com', 'Range': rng}


def get_good_filename(video):
    badchars =  ('?', '"', '>', '<', ':', '|', '\\', '/')
    goodname = ''
    for i in range(len(video)):
        if video[i] == ' ':
            goodname = f"{goodname}_"
        elif video[i] not in badchars:
            goodname = f"{goodname}{video[i]}"
    return f"{goodname}.mp4"
            



def download(username, password, urls, Logs):
    WebCli = WebClient(username, password, Logs)
    videos = []
    for addr in urls:
        Logs.log(f"Getting name and url of '{addr}'", 'blue')
        data = WebCli.get_url_and_filename(addr)
        if data[0] == 'Error':
            return
        videos.append(data)
    WebCli.close()
    if not os.path.isdir('Videos'):
        os.mkdir('Videos')
    os.chdir('Videos')
    s = requests.Session()
    i = 1
    for video in videos:
        Logs.log(f"Downloading video {i}: '{video[1]}'", 'blue')
        segments = get_segments(s, video[0])
        fullsize = int(segments[-1].split('-')[1])
        headers = gen_videodownload(segments[0])
        goodname = get_good_filename(video[1])
        file = open(goodname, 'wb')
        resp = reqncopy(s, video[0], headers, file, fullsize, Logs)
        Logs.log('Download complete', 'blue')
        file.close()
        i = i+1



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        logging.info("Please provide username and password")
    download(sys.argv[1], sys.argv[2])
