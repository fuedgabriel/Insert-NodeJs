import request
import wget


def DownloadVideo(url):
    try:
        responsee = requests.head(x, allow_redirects=True)
        wget.download(responsee.url, out=directory)
        return True
    except:
        print("Erro no Download do vídeo: " + url)
        return False
