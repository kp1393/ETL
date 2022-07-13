import requests
import json
import gspread
import numpy as np


class cidades():

# O método 'pesquisa' tem como objetivo auxiliar na busca pelo código IBGE a partir do nome da cidade    
    
    def pesquisa(cidade):
        lista={}
        r=requests.get("http://servicodados.ibge.gov.br/api/v1/localidades/municipios")
           
        #Verifica se a conexao foi bem sucedida
        if r.status_code == 200:
            
            arquivo_json = json.loads(r.text)
            j=0
            
            #REaliza a pesquisa e verifica se a cidade foi encontrada 
            for i in range(0,len(arquivo_json)):
                if cidade.upper() in arquivo_json[i]['nome'].upper():
                    nome_cidade = arquivo_json[i]['nome']
                    uf = arquivo_json[i]['microrregiao']['mesorregiao']['UF']['sigla']
                    codigo_ibge = arquivo_json[i]['id']
                
                    lista[j] = dict([('Cidade', nome_cidade), ('UF', uf), ('Codigo IBGE', codigo_ibge)])
                    j=j+1
        else:
            print("Erro! A API do IBGE não se encontra disponível no momento")
            
        return(lista)
                
# O método "dados_auxiliar" tem como objetivo fazer a requisição no site do IBGE e buscar as informações e retornar os dados em forma de string e de lista
# -História,Gentílico,Região,População,Renda e Escolaridade

    def dados_auxiliar(codigo_ibge):               
         
        dados_1=requests.get("https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun="+str(codigo_ibge))      
        dados_2=requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/25207/resultados/"+str(codigo_ibge))
        dados_3=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios/'+str(codigo_ibge))
        dados_4=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/47001/resultados/'+str(codigo_ibge))
        dados_5=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/60045/resultados/'+str(codigo_ibge))
        
        if dados_1.status_code != 200 or dados_2.status_code != 200 or dados_3.status_code != 200 or dados_4.status_code != 200 or dados_5.status_code != 200:
            print("Não foi possível encontrar os resultados buscados. As causas podem ser: \n [1] A API do IBGE não se encontra disponível no momento\n [2] O código inserido está incorreto. Consulte o método pesquisa() para auxiliar na busca")
            
            string=""
            conjunto=[]
        
        else:   
            
            nome = dados_1.json()[str(codigo_ibge)]['MUNICIPIO']
            historia = dados_1.json()[str(codigo_ibge)]['HISTORICO']
            gentilico = dados_1.json()[str(codigo_ibge)]['GENTILICO']
            populacao = dados_2.json()[0]['res'][0]['res']['2010'] 
            microrregiao = dados_3.json()['microrregiao']['nome']
            mesorregiao = dados_3.json()['microrregiao']['mesorregiao']['nome']
            uf = dados_3.json()['microrregiao']['mesorregiao']['UF']['sigla'] 
            pib_per_capta = dados_4.json()[0]['res'][0]['res']['2019']
            escolarizacao = dados_5.json()[0]['res'][0]['res']['2010']    
            string = 'Cidade:'+nome+'\n\nHistória da cidade: '+historia+"\n\nGentílico:"+gentilico+"\n\nPopulação:"+populacao+" habitantes"+"\n\nUF:"+uf+"\nMesorregião:"+mesorregiao+"\nMicrorregião:"+microrregiao+"\n\nPIB per capta: (R$) "+pib_per_capta+"\n\nTaxa de escolarização (6 a 14 anos): "+escolarizacao+" %"
            conjunto = [nome,historia,gentilico,populacao,microrregiao,mesorregiao,uf,pib_per_capta,escolarizacao]
              
        return string, conjunto
 

    def dados(codigo_ibge):
        
        if len(str(codigo_ibge))==7:
            
            info, lista = cidades.dados_auxiliar(codigo_ibge)
            
        else:
            info="Erro! O código deve conter 7 dígitos. Utilize o método pesquisa() para auxiliar na busca pela cidade!"        
       
        return(print(info))
        
    
# O método "dados_planilha" tem como objetivo escrever na planilha as informações extraídas do site do IBGEa partir dos códigos na coluna A
# LInk da planilha: https://docs.google.com/spreadsheets/d/18tOEpFhxAhtnYjEmEKyMcCj8X6nrf_4oal29Q13AmO8/

    def dados_planilha():
        lista_geral=[]
        
        # Autenticação a partir do arquivo json gerado pelo Google Cloud
        gc = gspread.service_account(filename='projeto-napp-f881b2552721.json')
        
        #Abrir a planilha pela ID
        planilha = gc.open_by_key('18tOEpFhxAhtnYjEmEKyMcCj8X6nrf_4oal29Q13AmO8')
        
        #ler a lista de códigos do IBGE da planilha
        codigos = planilha.worksheet('Dados').col_values(1)
        
        # Laço para fazer a requisção das informações por meio do método dados_auxiliar
        for i in range(1,len(codigos)):
            
            if len(str(codigos[i]))==7:
                info, lista = cidades.dados_auxiliar(codigos[i])
            
                lista_geral.append(lista)
            
                print(info)
                print("\n")
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            else:
                lista=[]
                lista_geral.append(lista)
                print("Cidade não encontrada! Verifique o código ", codigos[i])
       
        array = np.array(lista_geral)

        # Escreve os dados na planilha de destino
        planilha.worksheet('Dados').update('B2', array.tolist())


