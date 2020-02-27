import requests
import json
import wget
import _thread as thread
import threading

import os
import time
videos_titleBG = []
videos_urlBG = []
videos_mp4BG = []

videos_titleSD = []
videos_urlSD = []
videos_mp4SD = []

videos_titleHD = []
videos_urlHD = []
videos_mp4HD = []


def clear():
    videos_mp4SD.clear
    videos_titleSD.clear
    videos_urlSD.clear

    videos_mp4BG.clear
    videos_titleBG.clear
    videos_urlBG.clear

    videos_mp4HD.clear
    videos_titleHD.clear
    videos_urlHD.clear


def insert(title, episode, idAnime, url):
    payload = {
        "_id": str(idAnime),
        "Title": str(title),
        "Episodes": str(episode),
        "URL": str(url),
        "User": "Python"
    }
    requests.post('http://localhost:7844/api/animeErro', json=payload)


def GetPage():
    page = requests.get(
        'https://remainder.myvideo.vip/api-new/animes/1?search=all')
    if(page.status_code == 200):
        page = json.loads(page.content)
        return page['animes']['paginas']
    else:
        return False


def GetAllAnimes():
    page = str(GetPage())
    print(int(page[:-3])+1)
    for x in range(1, int(page[:-3])+1):
        print()
        print()
        print('*****************************')
        print('Página '+str(x))
        print('*****************************')
        print()
        print()
        try:
            url = 'https://remainder.myvideo.vip/api-new/animes/' + \
                str(x)+'?search=all'
            ListAnimes = requests.get(url)
            ListAnimes = json.loads(ListAnimes.content)
            if(ListAnimes == "{\"animes\":{}}"):
                insert('página', str(x), str(x), url)
                print('___________________________')
                print('Erro na página: '+str(x))
                print('___________________________')
            else:
                ListAnimes = ListAnimes['animes']['animes']
                for y in range(len(ListAnimes)):
                    print('id: '+str(ListAnimes[y]['id']))
                    print('Nome: '+str(ListAnimes[y]['nome']))
                    print('Numero da temporada: ' +
                          str(ListAnimes[y]['numTemporada']))
                    print('Temporada: '+str(ListAnimes[y]['temporada']))
                    print('Imagem: '+str(ListAnimes[y]['capa']))
                    print('_________________________________________________')
                    print()
                    print()
                    os.system('mkdir '+str(ListAnimes[y]['id']))
                    GetInfo(str(ListAnimes[y]['id']))
        except:
            insert('página', str(x), str(x), url)
            print('___________________________')
            print('Erro na página: '+str(x))
            print('___________________________')
            print()
            print()


def GetInfo(id):
    url = 'https://remainder.myvideo.vip/api-new/anime/'+str(id)
    info = requests.get(url)
    if(info.status_code == 200):
        info = json.loads(info.content)
        info = info['anime']
        dub = info['btn_dub']
        leg = info['btn_leg']
        img = info['capa']

        ep_leg = info['ep_leg']
        ep_dub = info['ep_dub']
        desc = info['ds']
        _id = info['id']
        year = info['lancamento']
        temp = info['numTemporada']
        status = info['producao']
        temp_name = info['temporada']
        category = []
        movie = []
        id_movie = []
        img_movie = []
        ovas = []
        ovas_id = []
        ovas_img = []

        for z in info['cat']:
            category.append(z['nome'])
        for z in info['filmes']:
            movie.append(z['nome'])
            id_movie.append(z['id'])
            img_movie.append(z['capa'])
        for z in info['ovas']:
            ovas.append(z['nome'])
            ovas_id.append(z['id'])
            ovas_img.append(z['capa'])
        if(dub == True):
            print()
            print('____________________________________________')
            print('Episódios dublado')
            GetEp(_id, '1', False, 'DUB')
            print('____________________________________________')
            print()
            print()
            print()
            print()

        if(leg == True):
            print()
            print('____________________________________________')
            print('Episódios legendado')
            GetEp(_id, '1', False, 'LEG')
            print('____________________________________________')
            print()
            print()
            print()
        input()
    else:
        return False


def GetEpOne(id, page, validator, language):
    url = 'https://remainder.myvideo.vip/api-new/eps/' + \
        str(id)+'/'+language+'/'+page+'?search=all'
    eps = requests.get(url)
    eps = json.loads(eps.content)
    eps = eps['eps']


def GetEp(id, page, validator, language):
    url = 'https://remainder.myvideo.vip/api-new/eps/' + \
        str(id)+'/'+language+'/'+page+'?search=all'
    eps = requests.get(url)
    eps = json.loads(eps.content)
    eps = eps['eps']

    if(validator == True):
        eps = eps['eps']
        for x in eps:
            print(x)
            if(x['link_bg'] == True):
                thread.start_new_thread(GetVideoBG, (x['id'],))
            if(x['link_hd'] == True):
                thread.start_new_thread(GetVideoHD, (x['id'],))
            if(x['link_sd'] == True):
                thread.start_new_thread(GetVideoSD, (x['id'],))
            print('_____________________')
        return 0

    if(eps['paginas'] > 1.9):
        pag = str(eps['paginas'])[:-3]
        for y in range(1, int(pag)+1):
            GetEp(str(id), str(y), True, language)
    else:
        pag = str(eps['paginas'])[:-3]
        GetEp(str(id), '1', True, language)

    tBG = threading.Thread(target=DownloadVideo, args=(
        videos_urlBG, videos_titleBG, videos_mp4BG, id, 'BG'))
    tSD = threading.Thread(target=DownloadVideo, args=(
        videos_urlSD, videos_titleSD, videos_mp4SD, id, 'SD'))
    tHD = threading.Thread(target=DownloadVideo, args=(
        videos_urlHD, videos_titleHD, videos_mp4HD, id, 'HD'))
    tBG.start()
    tSD.start()
    tHD.start()
    while True:
        if(tSD.isAlive() == False and tBG.isAlive() == False and tHD.isAlive() == False):
            print('Download finalizado')
            break
        else:
            print('\nBG: '+str(tBG.isAlive()))
            print('SD: '+str(tSD.isAlive()))
            print('HD: '+str(tHD.isAlive()))
            print('Download em andamento')
            time.sleep(10)

    input()
    clear()


def GetVideoBG(id_ep):
    # print('Video url'+str(videos_url))
    url = 'https://remainder.myvideo.vip/api-new/assistindov2/BG/' + \
        str(id_ep)+'/PLAYER-2/c7e5767ead45d629'
    video = requests.get(url)
    video = json.loads(video.content)
    video = video['requestedMP4']
    videos_titleBG.append(video['title'])
    videos_urlBG.append(video['download'])
    videos_mp4BG.append(video['mp4'])
    return videos_mp4BG


def GetVideoSD(id_ep):
    # print('Video url'+str(videos_url))
    url = 'https://remainder.myvideo.vip/api-new/assistindov2/SD/' + \
        str(id_ep)+'/PLAYER-2/c7e5767ead45d629'
    video = requests.get(url)
    video = json.loads(video.content)
    video = video['requestedMP4']
    videos_titleSD.append(video['title'])
    videos_urlSD.append(video['download'])
    videos_mp4SD.append(video['mp4'])
    return videos_titleSD


def GetVideoHD(id_ep):
    # print('Video url'+str(videos_url))
    url = 'https://remainder.myvideo.vip/api-new/assistindov2/HD/' + \
        str(id_ep)+'/PLAYER-2/c7e5767ead45d629'
    video = requests.get(url)
    video = json.loads(video.content)
    video = video['requestedMP4']
    videos_titleHD.append(video['title'])
    videos_urlHD.append(video['download'])
    videos_mp4HD.append(video['mp4'])
    return videos_titleHD


def DownloadVideo(url, title, mp4, _id, quality):

    if(url == []):
        return False
    os.system('cd '+str(_id)+' && mkdir '+quality)
    # print(url)
    print('Iniciando download')
    for x in url:
        print('URL: {'+str(x) + '}')
        try:
            responsee = requests.head(x, allow_redirects=True)
            wget.download(responsee.url)
        except:
            insert('Episode', str(quality), str(_id), str(x))


# GetEp(str(12), '1', False, 'LEG')
GetAllAnimes()
