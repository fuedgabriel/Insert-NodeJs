import requests
import json
import wget
import threading
import os
import time
import requestImage
import speedtest


videos_titleBG = []
videos_urlBG = []
videos_mp4BG = []

videos_titleSD = []
videos_urlSD = []
videos_mp4SD = []

videos_titleHD = []
videos_urlHD = []
videos_mp4HD = []

Year = ["Null"]
EpisodesLEG = [0]
EpisodesDUB = [0]
EpisodeLEG = [0]
EpisodeDUB = [0]
Ovass = [0]
Movies = [0]
Quality = ["Null"]
Category = ["Null"]
Anime = ["null"]
Anime_id = ["Null"]
DownloadBG = ["Null"]
DownloadSD = ["Null"]
DownloadHD = ["Null"]
ErrosPage = ["0"]
PageLocal = ["Null"]
Banner = ["Null"]

Download = [0]
Upload = [0]
Ping = [0]


def test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    Download.clear()
    Download.append(res["download"])
    Upload.clear()
    Upload.append(res["upload"])
    Ping.clear()
    Ping.append(res["ping"])
    time.sleep(600)


def Control():
    tSpeed = threading.Thread(target=test, args=())
    tSpeed.start()

    while True:
        time.sleep(2)
        os.system('cls')
        print(
            "\033[31m***************-----\033[0;0m\033[33mPAINEL DE CONTROLE\033[31m-----***************\033[0;0m \033[32mPágina: \033[4;33;40m" + str(PageLocal[0])+"\033[41;0m")
        print("                                 \033[33m Download: \033[31m" +
              str(Download[0]/1000)[0:2]+" \033[33m Upload: \033[31m"+str(Upload[0]/1000)[0:2]+" \033[33m  Ping: \033[31m"+str(Ping[0])[0:1])
        print("\nNome: \033[35m"+str(Anime[0])+"\033[35;0m           Id: \033[36m" +
              str(Anime_id[0])+"\033[36;0m   Ano: " + str(Year[0]))
        print("Legendado: "+str(EpisodesLEG[0])+" de "+str(EpisodeLEG[0]))
        print("Dublado: "+str(EpisodesDUB[0])+" de "+str(EpisodeDUB[0]))
        print("Qualidades --> BG: " +
              DownloadBG[0]+"   SD: "+DownloadSD[0]+"   HD: "+DownloadHD[0])
        print("Banner: "+Banner[0]+"")
        print("Ovas: " +
              str(Ovass).replace('[', '').replace(']', '').replace('\'', ''))
        print("Filmes: " +
              str(Movies).replace('[', '').replace(']', '').replace('\'', ''))
        print("Categorias: " +
              str(Category).replace('[', '').replace(']', '').replace('\'', ''))
        print("Páginas com erro: \033[31m" +
              str(ErrosPage).replace('[', '').replace(']', '').replace('\'', '') + "\033[0;0m")


def GoogleStorage():
    pub = "gsutil acl ch -u AllUsers:R gs://my-awesome-bucket/kitten.png"
    upload = "gsutil cp http://svr1---s551-xjgk1ahg-cdn.gvideo.g-storage.network/animes/b-4/animes/naruto-shippunden/legendado/hd/326.mp4?rm=ZOYWkVSQeeMkI1f9vLY2QA&rf=1583002037 gs://animese0storage"
    uploadFolder = "gsutil cp -r 1484 gs://animese0storage/Animes/animes"


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
        "Title": str(title),
        "Anime_id": str(idAnime),
        "Episodes": str(episode),
        "URL": str(url),
        "User": "Python"
    }
    requests.post('http://localhost:7844/api/animeErro', json=payload)


def insertNoID(title, episode, url):
    payload = {
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
    # print(int(page[:-3])+1)
    for x in range(1, int(page[:-3])+1):
        PageLocal.clear()
        PageLocal.append(x)

        # print()
        # print()
        # print('*****************************')
        # print('Página '+str(x))
        # print('*****************************')
        # print()
        # print()
        try:
            url = 'https://remainder.myvideo.vip/api-new/animes/' + \
                str(x)+'?search=all'
            ListAnimes = requests.get(url)
            ListAnimes = json.loads(ListAnimes.content)
            if(ListAnimes == "{\"animes\":{}}"):
                insertNoID('pages', x, url)
                ErrosPage.append(x)
                # print('___________________________')
                # print('Erro na página: '+str(x))
                # print('___________________________')
            else:
                ListAnimes = ListAnimes['animes']['animes']
                for y in range(len(ListAnimes)):
                    # print('id: '+str(ListAnimes[y]['id']))
                    # print('Nome: '+str(ListAnimes[y]['nome']))
                    # print('Numero da temporada: ' +
                    #       str(ListAnimes[y]['numTemporada']))
                    # print('Temporada: '+str(ListAnimes[y]['temporada']))
                    # print('Imagem: '+str(ListAnimes[y]['capa']))
                    # print('_________________________________________________')
                    # print()
                    # print()
                    os.system('mkdir '+str(ListAnimes[y]['id']))
                    GetInfo(str(ListAnimes[y]['id']), ListAnimes[y]['nome'])
        except:
            ErrosPage.append(x)
            insertNoID('página', x, url)
            # print('___________________________')
            # print('Erro na página: '+str(x))
            # print('___________________________')
            # print()
            # print()


def GetInfo(id, name):
    try:
        url = 'https://remainder.myvideo.vip/api-new/anime/'+str(id)
        info = requests.get(url)
        if(info.status_code == 200):
            bannner = requestImage.GETimage(name)
            Banner.clear()
            if(bannner == False):
                Banner.append("\033[31mErro na requisição\033[0;0m")
            else:
                Banner.append("\033[32mSucesso na requisição\033[32;0m")

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
            Year.clear()
            Anime_id.clear()
            EpisodeDUB.clear()
            EpisodeLEG.clear()
            Category.clear()
            Anime.clear()
            Ovass.clear()
            Movies.clear()
            EpisodesDUB.clear()
            EpisodesLEG.clear()

            EpisodesLEG.append(0)
            EpisodesDUB.append(0)
            Movies.append(len(id_movie))
            Ovass.append(len(ovas_id))
            Anime.append(name)
            Anime_id.append(id)
            EpisodeLEG.append(ep_leg)
            EpisodeDUB.append(ep_dub)
            Year.append(year)
            Category.append(category)
            if(dub == True):
                # print()
                # print('____________________________________________')
                # print('Episódios dublado')
                GetEp(_id, '1', False, 'DUB', name)
                # print('____________________________________________')
                # print()
                # print()
                # print()
                # print()

            if(leg == True):
                # print()
                # print('____________________________________________')
                # print('Episódios legendado')
                GetEp(_id, '1', False, 'LEG', name)
                # print('____________________________________________')
                # print()
                # print()
                # print()
                # input()
        else:
            insert('Anime', id, id, url)
            return False
    except:
        insert('Anime', id, id, url)


def GetEpOne(id, page, validator, language):
    url = 'https://remainder.myvideo.vip/api-new/eps/' + \
        str(id)+'/'+language+'/'+page+'?search=all'
    eps = requests.get(url)
    eps = json.loads(eps.content)
    eps = eps['eps']


def GetEp(id, page, validator, language, name):
    url = 'https://remainder.myvideo.vip/api-new/eps/' + \
        str(id)+'/'+language+'/'+page+'?search=all'
    eps = requests.get(url)
    eps = json.loads(eps.content)
    eps = eps['eps']

    if(validator == True):
        eps = eps['eps']
        for x in eps:
            # print(x)
            HD = False
            SD = False
            if(x['link_hd'] == True):
                tLINKhd = threading.Thread(target=GetVideoHD, args=(x['id'],))
                tLINKhd.start()
                HD = True
            if(x['link_sd'] == True and HD != True):
                tLINKsd = threading.Thread(target=GetVideoSD, args=(x['id'],))
                tLINKsd.start()
                SD = True
            if(x['link_bg'] == True and SD != True):
                tLINKbg = threading.Thread(target=GetVideoBG, args=(x['id'],))
                tLINKbg.start()

            # print('_____________________')
        return 0

    if(eps['paginas'] > 1.9):
        pag = str(eps['paginas'])[:-3]
        for y in range(1, int(pag)+1):
            GetEp(str(id), str(y), True, language, name)
    else:
        pag = str(eps['paginas'])[:-3]
        GetEp(str(id), '1', True, language, name)

    tBG = threading.Thread(target=DownloadVideo, args=(
        videos_urlBG, videos_titleBG, videos_mp4BG, id, 'BG', language, name))
    tSD = threading.Thread(target=DownloadVideo, args=(
        videos_urlSD, videos_titleSD, videos_mp4SD, id, 'SD', language, name))
    tHD = threading.Thread(target=DownloadVideo, args=(
        videos_urlHD, videos_titleHD, videos_mp4HD, id, 'HD', language, name))
    tBG.start()
    tSD.start()
    tHD.start()
    while True:
        if(tSD.is_alive() == False and tBG.is_alive() == False and tHD.is_alive() == False):
            DownloadBG.clear()
            DownloadSD.clear()
            DownloadHD.clear()
            DownloadBG.append(" \033[32m Finalizado \033[32;0m")
            DownloadSD.append(" \033[32m Finalizado \033[32;0m")
            DownloadHD.append(" \033[32m Finalizado \033[32;0m")
            # print('\nDownload finalizado')
            break
        else:
            # print('\nBG: '+str(tBG.is_alive()))
            # print('SD: '+str(tSD.is_alive()))
            # print('HD: '+str(tHD.is_alive()))
            # print('Download em andamento')
            if(tBG.is_alive() == True):
                DownloadBG.clear()
                DownloadBG.append("\033[34mEm andamento \033[34;0m")
            else:
                DownloadBG.clear()
                DownloadBG.append(" \033[32m Finalizado \033[32;0m")

            if(tSD.is_alive() == True):
                DownloadSD.clear()
                DownloadSD.append("\033[34mEm andamento \033[34;0m")
            else:
                DownloadSD.clear()
                DownloadSD.append(" \033[32m Finalizado \033[32;0m")

            if(tHD.is_alive() == True):
                DownloadHD.clear()
                DownloadHD.append("\033[34mEm andamento \033[34;0m")
            else:
                DownloadHD.clear()
                DownloadHD.append(" \033[32m Finalizado \033[32;0m")

            time.sleep(3)
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


def DownloadVideo(url, title, mp4, _id, quality, language, name):
    if(url == []):
        return False
    os.system('cd '+str(_id)+' && mkdir '+quality)
    os.system('cd '+str(_id)+' && echo "nome":"'+str(name) +
              '", "episodes":"'+str(title)+'">nome.json')

    directory = str(_id)+'/'+quality+'/'
    # print(url)
    # print('Iniciando download')
    zz = 0
    for x in url:
        zz = zz+1
        if(quality == 'BG'):
            directory = str(_id)+'/'+quality+'/'
            directory = directory+str(zz)+'.mp4'
        if(language == 'LEG'):
            EpisodesLEG.clear()
            EpisodesLEG.append(zz)
        else:
            EpisodesDUB.clear()
            EpisodesDUB.append(zz)

        # print('URL: {'+str(x) + '}')
        try:
            # print("Download concluido :"+str(x))
            responsee = requests.head(x, allow_redirects=True)
            wget.download(responsee.url, out=directory)
        except:
            insert('Episode '+quality+' '+language, zz, _id, x)


# GetEp(str(12), '1', False, 'LEG')
threading._start_new_thread(Control)
GetAllAnimes()
