import requests
import json

# O método "dados" tem como objetivo fazer a requisição no site do IBGE e buscar as seguintes informações de uma determinada cidade: 
# -História
# -Gentílico
# -Região
# -População
# -Renda
# -Escolaridade

def dados(codigo_ibge):


    dados_1=requests.get("https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun="+str(codigo_ibge)).json()

    historia = dados_1[str(codigo_ibge)]['HISTORICO']

    gentilico = dados_1[str(codigo_ibge)]['GENTILICO']

    dados_2=requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/25207/resultados/"+str(codigo_ibge)).json()

    populacao = dados_2[0]['res'][0]['res']['2010']
    
    
    return(historia,gentilico,populacao)

teste=dados(3526704)
teste
