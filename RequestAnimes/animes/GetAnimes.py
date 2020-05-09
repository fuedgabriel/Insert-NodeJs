import requests
import json


def Animes(id):
    url = "https://remainder.myvideo.vip/api-new/anime/" + str(id)
    anime = json.loads(requests.get(url).content)
    print(anime)
