import requests
import json


def dados(codigo_ibge):


    pagina_cidade=requests.get("https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun="+str(codigo_ibge)).json()

    historia = pagina_cidade[str(codigo_ibge)]['HISTORICO']

    gentilico = pagina_cidade[str(codigo_ibge)]['GENTILICO']

    pagina_cidade=requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/25207/resultados/"+str(codigo_ibge)).json()

    populacao = pagina_cidade[0]['res'][0]['res']['2010']
    
    
    return(historia,gentilico,populacao)

teste=dados(3526704)
teste
