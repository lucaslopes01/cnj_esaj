import requests
from datetime import datetime, timedelta
import json
import time
from utils.class_mongo import Mongo
from decouple import config
mongo = Mongo(config('MONGO_USR'), config('MONGO_PWD'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB_ESAJ'), ambiente='DEV')
mongo_2 = Mongo(config('MONGO_USR'), config('MONGO_PWD'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB_ESAJ'), ambiente='DEV')
mongo.getcoll('processos_esaj_cnj')
mongo_2.getcoll('esaj_principal')
ultimo_process= list(mongo._return_sort({},'_id'))[0]
# from utils.rabbitmq import RabbitMQ
data_base = datetime.strptime(ultimo_process['data_cnj'], "%d/%m/%Y")
hoje = datetime.now()
def valida_resposta(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://comunica.pje.jus.br/',
        'Origin': 'https://comunica.pje.jus.br',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive'
    }

    max_tentativas = 20
    intervalo = 3  # segundos

    ultima_resposta = None

    for tentativa in range(1, max_tentativas + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            ultima_resposta = resp

            # sucesso
            if resp.status_code == 200:
                return resp

            # qualquer erro != 200 → retry
            if tentativa < max_tentativas:
                time.sleep(intervalo)
                continue

            # última tentativa: retorna o que veio
            return resp

        except requests.exceptions.RequestException as e:
            # erro de rede / timeout / conexão
            if tentativa < max_tentativas:
                time.sleep(intervalo)
                continue
            raise  # estoura o erro na última tentativa

    return ultima_resposta

while True:
        time.sleep(1)
        dia = str(data_base.day)
        mes = str(data_base.month)
        ano = str(data_base.year)
        aux = 1
        data_base_string = data_base.strftime("%d/%m/%Y")
        while True:
            url = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?pagina={aux}&itensPorPagina=5&siglaTribunal=TJSP&dataDisponibilizacaoInicio={data_base.year}-{data_base.month}-{data_base.day}&dataDisponibilizacaoFim={data_base.year}-{data_base.month}-{data_base.day}"
            # url = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?pagina={aux}&itensPorPagina=100&texto=UNIAO+FEDERAL&siglaTribunal=TRF3&dataDisponibilizacaoInicio={data_base.year}-{data_base.month}-{data_base.day}&dataDisponibilizacaoFim={data_base.year}-{data_base.month}-{data_base.day}"

            response =valida_resposta(url)
            # valida_resposta = re
            resposta =  json.loads(response.text)
            if not resposta['items'] :
                break
            else:
                for i in resposta['items']:
                     if not i['nomeOrgao'].find("JEF")>-1:
                        if i['nomeClasse'].lower().find('cumprimento de sentença')>-1:
                            processo = list(mongo._return_query({"processo":i["numeroprocessocommascara"]}))
                            processo_2 = list(mongo_2._return_query({"processo":i["numeroprocessocommascara"]}))
                            if not processo and not processo_2:
                                mongo._add_one({"processo":i["numeroprocessocommascara"], "data_cnj":data_base_string,"status":"aguardando", "pag":aux})
                                print(i["numeroprocessocommascara"], 'inserido')
                if aux == 2000:
                    break
                aux +=1
             
        if data_base > hoje:
            break
        else:
            data_base = data_base+ timedelta(days=1)

        
        
