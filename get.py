import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def DataGinanimaEpisode(output, nome):
    animeId = requests.get('http://127.0.0.1:7844/api/anime')
    animeId = json.loads(animeId.content)
    for ado in animeId:
        if(str(nome) == ado['Title']):
            _id = ado['_id']
            break
        else:
            pass
    x = 0
    for episodes in output:
        try:
            x = x+1
            id = episodes['Id']
            # episode = episodes['Nome']
            request = requests.get(
                'http://one.zetai.info/api/episodioexes/links?id='+str(id))
            link = json.loads(request.content)
            try:
                if('SD/MQ' in link[0]['Nome']):
                    episodio = link[0]['Endereco']
            except:
                pass
            try:
                if('SD/HQ' in link[1]['Nome']):
                    episodio = link[1]['Endereco']
            except:
                pass
            try:
                if('Hd' in link[2]['Nome']):
                    episodio = link[2]['Endereco']
            except:
                pass

            payload = {
                "idAnime": str(_id),
                "title": str(nome),
                "url": str(episodio),
                "episode": str(x),
                "season": "1",
                "user": "Python"
            }
            a = requests.post('http://localhost:7844/api/video/', json=payload)
        except:
            print('Erro em ep :'+str(x) + '  Nome:' + str(nome))


def DataGiganima():
    for x in range(1, 999999):
        try:
            requestDesc = requests.get(
                'http://one.zetai.info/odata/Animesdb/?$skip='+str(x)
            )

            DescJson = json.loads(requestDesc.content)

            for desc in DescJson['value']:
                id = desc['Id']
                nameG = desc['Nome']
                descriG = desc['Desc']

                if(desc['Status'] == True):
                    statusG = 'Lançamento'
                else:
                    statusG = 'Encerrado'
                ano = desc['Ano']
                imagem = desc['Imagem']
                # categoria = desc['Categoria']
                print('Id:' + str(id))
                print('Nome:' + str(nameG))
                # print('Descricao: '+str(desc))
                print('Status: ' + str(statusG))
                print('Imagem: ' + str(imagem))
                req = requests.get(
                    'http://one.zetai.info/api/episodioexes/'+str(id))
                output = json.loads(req.content)
                ep = (len(output)+1)

                animeId = requests.get('http://127.0.0.1:7844/api/anime')
                animeId = json.loads(animeId.content)
                for ado in animeId:

                    if(str(nameG) == ado['Title']):
                        bb = '1'
                        break
                    else:
                        bb = '2'
                        pass
                payload = {
                    'Title': str(nameG),
                    'English': str(nameG),
                    'Japanese': str(nameG),
                    'Synopse': str(descriG),
                    'Seasons': 1,
                    'Status': str(statusG),
                    'Category': '5de1d75c43c6f33cf8f9331f',
                    'Studio': 'Bee Train',
                    'Episodes': ep,
                    'Score': 8.23,
                    'air': str(ano)+'-07-01',
                    'age': '16',
                    'url': str(imagem)
                }
                if(bb == '2'):

                    a = requests.post(
                        'http://127.0.0.1:7844/api/anime/', json=payload)
                    DataGinanimaEpisode(output, nameG)
                else:
                    print('Já existe no banco de dados')
                #print('Código da requisição: ' + str(a.status_code))
                # print(a)

        except:
            print('Erro no numero ' + str(x))


DataGiganima()


def DataAnime(nome):

    driver = webdriver.Chrome()

    requestDesc = requests.get('http://one.zetai.info/odata/Animesdb/?$skip=1')
    DescJson = json.loads(requestDesc.content)
    driver.get('http://anisearch.outrance.pl/?task=search&query=' +
               nome.replace(' ', '+'))
    saida = driver.page_source
    sopa = BeautifulSoup(saida, 'html.parser')
    link = sopa.find_all("a", href=True)
    link = str(link[0]).split('"')
    driver.get(link[1])
    print(link[1])
    print('________________________________')
