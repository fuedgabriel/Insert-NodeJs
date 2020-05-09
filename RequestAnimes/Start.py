import requests
import json
import wget
import threading
import os
import time
import speedtest
# Bibliotecas
from animes import GetAnimes


videos_titleHD = []
videos_urlHD = []
videos_mp4HD = []
Download = "0"
Upload = "0"
Ping = "0"


def test():
    global Download
    global Upload
    global Ping
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    Download = res["download"]
    Upload = res["upload"]
    Ping = res["ping"]
    time.sleep(600)


def GetPage(id):
    url = 'https://remainder.myvideo.vip/api-new/animes/'+str(id)+'?search=all'
    Page = json.loads(requests.get(url).content)
    if(Page == "{\"animes\":{}}"):
        return False
    else:
        return Page['animes']['animes']


def GetAllAnimes():
    for x in range(1, 108):  # tem que colocar um a mais do número de páginas da API "https://remainder.myvideo.vip/api-new/animes/1?search=all"
        page = GetPage(x)
        for AnimeId in page:  # :1 é a posição em que o id está no json
            GetAnimes.Animes(AnimeId['id'])
            input()


def Control():
    tSpeed = threading.Thread(target=test, args=())
    tSpeed.start()
    while True:
        time.sleep(2)
        GetAllAnimes()


GetAllAnimes()
