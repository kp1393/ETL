import requests
import json
import gspread
import numpy as np


class cidades():

# O método 'pesquisa' tem como objetivo auxiliar na busca pelo código IBGE a partir do nome da cidade    
    
    def pesquisa():
        lista= []
        r=requests.get("http://servicodados.ibge.gov.br/api/v1/localidades/municipios")

        arquivo_json = json.loads(r.text)
    
        cidade = str(input("Digite o nome da cidade: "))
    
        for i in range(0,len(arquivo_json)):
            if cidade.upper() in arquivo_json[i]['nome'].upper():
                nome_cidade = arquivo_json[i]['nome']
                uf = arquivo_json[i]['microrregiao']['mesorregiao']['UF']['sigla']
                codigo_ibge = arquivo_json[i]['id']
            
                lista.append((nome_cidade,uf,codigo_ibge))
    
        return(lista)



# O método "dados_auxiliar" tem como objetivo fazer a requisição no site do IBGE e buscar as informações e retornar os dados em forma de string e de lista
# -História,Gentílico,Região,População,Renda e Escolaridade

    def dados_auxiliar(codigo_ibge):
            
        try:        
            dados_1=requests.get("https://servicodados.ibge.gov.br/api/v1/biblioteca?aspas=3&codmun="+str(codigo_ibge)).json()          
            dados_2=requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/25207/resultados/"+str(codigo_ibge)).json()
            dados_3=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios/'+str(codigo_ibge)).json()
            dados_4=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/47001/resultados/'+str(codigo_ibge)).json()
            dados_5=requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/60045/resultados/'+str(codigo_ibge)).json()
            
            
            try:
                nome = dados_1[str(codigo_ibge)]['MUNICIPIO']
            except:
                nome = "Nome da cidade não encontrada"            
            try:
                historia = dados_1[str(codigo_ibge)]['HISTORICO']
            except:
                historia = "História não encontrada"
            try:
                gentilico = dados_1[str(codigo_ibge)]['GENTILICO']
            except:
                gentilico = "Gentilico não encontrado"
            try:       
                populacao = dados_2[0]['res'][0]['res']['2010'] 
            except:
                populacao="População não encontrada"
            try:
                microrregiao = dados_3['microrregiao']['nome']
            except:
                microrregiao="Microrregião não encontrada"
            try:
                mesorregiao = dados_3['microrregiao']['mesorregiao']['nome']
            except:
                mesorregiao="Mesorregião não encontrada"
            try:
                uf = dados_3['microrregiao']['mesorregiao']['UF']['sigla'] 
            except:
                uf = "UF não encontrada"
            try:
                pib_per_capta = dados_4[0]['res'][0]['res']['2019']
            except:
                pib_per_capta="PIB er capta não encontrado"
            try:
                escolarizacao = dados_5[0]['res'][0]['res']['2010']    
            except:
                "Escolarização não encontrada"
        
            string = 'Cidade:'+nome+'\n\nHistória da cidade: '+historia+"\n\nGentílico:"+gentilico+"\n\nPopulação:"+populacao+" habitantes"+"\n\nUF:"+uf+"\nMesorregião:"+mesorregiao+"\nMicrorregião:"+microrregiao+"\n\nPIB per capta: (R$) "+pib_per_capta+"\n\nTaxa de escolarização (6 a 14 anos): "+escolarizacao+" %"
            
            conjunto = [nome,historia,gentilico,populacao,microrregiao,mesorregiao,uf,pib_per_capta,escolarizacao]
        except:
            string = "Erro 404. Verifique o código "+codigo_ibge
            conjunto=[]
            
        return string, conjunto
 


    def dados(codigo_ibge):
        
        if len(str(codigo_ibge))==7:
            
            info, lista = cidades.dados_auxiliar(codigo_ibge)
            
        else:
            info="Cidade não encontrada! Verifique o código "+codigo_ibge
        
        return(info)
        
    
# O método "dados_planilha" tem como objetivo escrever na planilha online os dados pesquisados no site do IBGE

    def dados_planilha():
        lista_geral=[]
        
        # Autenticação
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


