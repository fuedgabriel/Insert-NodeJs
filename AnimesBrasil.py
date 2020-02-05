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
        ListAnimes = requests.get(
            'https://remainder.myvideo.vip/api-new/animes/'+str(x)+'?search=all')
        ListAnimes = json.loads(ListAnimes.content)
        ListAnimes = ListAnimes['animes']['animes']
        for y in range(len(ListAnimes)):
            print('id: '+str(ListAnimes[y]['id']))
            print('Nome: '+str(ListAnimes[y]['nome']))
            print('Numero da temporada: '+str(ListAnimes[y]['numTemporada']))
            print('Temporada: '+str(ListAnimes[y]['temporada']))
            print('Imagem: '+str(ListAnimes[y]['capa']))
            print('_________________________________________________')
            print()
            print()

        input()


GetAllAnimes()
