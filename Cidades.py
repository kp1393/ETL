import requests
import json


class cidades():
    
# O método "dados" tem como objetivo fazer a requisição no site do IBGE e buscar as seguintes informações de uma determinada cidade: 
# -História,Gentílico,Região,População,Renda e Escolaridade

    def dados(codigo_ibge):

        dados_1=requests.get("https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun="+str(codigo_ibge)).json()
        dados_2=requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/25207/resultados/"+str(codigo_ibge)).json()
        dados_3=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios/'+str(codigo_ibge)).json()
        dados_4=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/47001/resultados/'+str(codigo_ibge)).json()
        dados_5=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/60045/resultados/'+str(codigo_ibge)).json()
        
        historia = dados_1[str(codigo_ibge)]['HISTORICO']
        gentilico = dados_1[str(codigo_ibge)]['GENTILICO']
        populacao = dados_2[0]['res'][0]['res']['2010'] 
        
        microrregiao = dados_3['microrregiao']['nome']
        mesorregiao = dados_3['microrregiao']['mesorregiao']['nome']
        uf = dados_3['microrregiao']['mesorregiao']['UF']['sigla'] 
        
        pib_per_capta = dados_4[0]['res'][0]['res']['2019']
        
        escolarizacao = dados_5[0]['res'][0]['res']['2010']
        
        info = 'História da cidade:\n\n'+ historia+"\n\nGentílico:" + gentilico +"\n\nPopulação:"+populacao+"\n\nUF:"+uf+"\nMesorregião:"+mesorregiao+"\nMcrorregião:"+microrregiao+"\n\nPIB per capta (R$):"+pib_per_capta+"\n\nTaxa de escolarização (6 a 14 anos): "+escolarizacao+" %"
        
        return(print(info))
        
    
# O método "dados_planilha" tem como objetivo fazer leitura de vários códigos em uma planilha online, fazer a requisição 
# no site do IBGE e escrever na mesma planilha as seguintes informações:
# -História,Gentílico,Região,População,Renda e Escolaridade    

    #def dados_planilha():
        
        # Códifgo em desnvolvimento
        
        
#teste=cidades.dados(3526704)
#teste
