import requests
import json


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
    for x in range(1, int(page[:-2])+1):
        print()
        print()
        print('*****************************')
        print('Página '+str(x))
        print('*****************************')
        print()
        print()
        ListAnimes = requests.get(
            'https://remainder.myvideo.vip/api-new/animes/'+str(x)+'?search=all')
        ListAnimes = json.loads(ListAnimes.content)
        try:
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
        except:
            print('___________________________')
            print('Erro na página: '+str(x))
            print('___________________________')
            print()
            print()
            input()


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
            GetEp(_id, '1', False, 'DUB')
            print('Episódio dublado acima')
        if(leg == True):
            GetEp(_id, '1', False, 'LEG')
            print('Episódio legendado acima')

    else:
        return False


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
                GetVideo(x['id'], 'BG')
            if(x['link_hd'] == True):
                GetVideo(x['id'], 'HD')
            if(x['link_sd'] == True):
                GetVideo(x['id'], 'SD')
            print('_____________________')
        return 0
    if(eps['paginas'] > 1):
        pag = str(eps['paginas'])[:-3]
        for y in range(1, int(pag)+1):
            GetEp(str(id), str(y), True, language)


def GetVideo(id_ep, quality):
    url = 'https://remainder.myvideo.vip/api-new/assistindov2/' + \
        str(quality)+'/'+str(id_ep)+'/PLAYER-2/c7e5767ead45d629'
    video = requests.get(url)
    video = json.loads(video.content)
    video = video['requestedMP4']
    print('Download: '+video['download'])
    print('MP4: '+video['mp4'])
    print('Title: '+video['title'])
    print('Url:'+video['url'])


GetEp(str(43), '1', False, 'LEG')
