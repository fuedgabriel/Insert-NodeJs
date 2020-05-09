from bs4 import BeautifulSoup
import urllib.request
import requests
import re


def GETimage(name):
    try:
        url = "https://anidb.net/anime/?adb.search=" + \
            str(name)+"&do.update=Search&noalias=1"
        responsee = requests.head(url, allow_redirects=True)
        req = urllib.request.Request(responsee.url, data=None, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        html = urllib.request.urlopen(req)
        bs = BeautifulSoup(html, 'html.parser')
        a = bs.find('img', class_='g_image g_bubble')
        return a['src']

    except:
        False


GETimage("7 seeds")
