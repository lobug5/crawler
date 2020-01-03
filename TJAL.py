import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import os.path

process_number = '0000575-40.2014.8.02.0081'
date_today = date.today()
file_name = str(date_today) + '_' + process_number + '.json'

def persist_crawler(name):
    if os.path.exists('search/'+ name):
        open(os.path.join('search', name), 'r')
        return
    else:
        # Parâmetros da busca
        url = "https://www2.tjal.jus.br/cpopg/open.do"
        find_url = "https://www2.tjal.jus.br/cpopg/search.do?conversationId=&dadosConsulta.localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=SAJ&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.valorConsultaNuUnificado=&dadosConsulta.valorConsulta=" + process_number + "&uuidCaptcha="
        # Declarando os parametros da biblioteca BeautifulSoup
        session = requests.session()
        session.get(url)
        response = session.get(find_url)
        soup = BeautifulSoup(response.content, "lxml")
        main_table = soup.findAll("table", {"class": "secaoFormBody"})

        print(response)

        def get_data(name):
            tr_list = soup.select("table.secaoFormBody tr")
            for tr in tr_list:
                td = tr.find('td')
                if td.text.strip() == name:
                    return td.find_next_sibling('td').text.strip()

        def get_parts_process(name):
            tr_list = soup.select("table#tablePartesPrincipais tr")
            span_list = soup.findAll("span", {"class": "mensagemExibindo"})
            for tr in tr_list:
                td = tr.find('td')
                if td.text.strip() == name:
                    return td.find_next_sibling('td').text.strip()

        def list_moviments_process(list1, list2):
            moviments = []
            for list1, list2 in zip(list1, list2):
                moviments.append(list1)
                moviments.append(list2)

            return moviments


        # Lista de Parâmetros
        process = get_data('Processo:')
        classe = get_data('Classe:')
        subject = get_data('Assunto:')
        distribuition = get_data('Distribuição:')
        control = get_data('Controle:')
        judge = get_data('Juiz:')
        action_value = get_data('Valor da ação:')
        demandante = get_parts_process('Demandante:')
        demandado = get_parts_process('Demandado:')
        advogado = get_parts_process('Advogado:')
        autora = get_parts_process('Autora:')
        reu = get_parts_process('Réu:')
        requerente = get_parts_process('Requerente:')

        # Montando o objeto com os dados extraidos
        information_process = {}

        information_process['processo'] = process
        information_process['classe'] = classe
        information_process['assunto'] = subject
        information_process['distribuicao'] = distribuition
        information_process['controle'] = control
        information_process['juiz'] = judge
        information_process['valor_acao'] = action_value

        parts_process = {}
        parts_process['demandante'] = demandante
        parts_process['demandado'] = demandado
        parts_process['advogado'] = advogado
        parts_process['requerente'] = requerente
        parts_process['autora'] = autora
        parts_process['reu'] = reu

        moviments_process = []
        moviment_class_fundoClaro = []
        moviment_class_fundoEscuro = []

        movements_elements = soup.findAll("tbody", {"id": "tabelaTodasMovimentacoes"})
            
        for element_moviment in movements_elements:
            list_content_moviment = element_moviment.text.strip()
            list_class_fundoClaro = element_moviment.findAll("tr", {"class": "fundoClaro"})
            list_class_fundoEscuro = element_moviment.findAll("tr", {"class": "fundoEscuro"})
            
        for movement in list_class_fundoClaro:
            moviment_class_fundoClaro.append(movement.text.strip())

        for movement in list_class_fundoEscuro:
            moviment_class_fundoEscuro.append(movement.text.strip())


        moviments_process = list_moviments_process(moviment_class_fundoClaro,moviment_class_fundoEscuro)

        # Montando o objeto principal 
        data = {}
        data['dados_processo'] = information_process
        data['partes_processo'] = parts_process
        data['movimentacao_processo'] = moviments_process

        # Exportando arquivo JSON
        date_today = date.today()
        file_name = str(date_today) + '_' + process_number + '.json'
        with open(os.path.join('search', file_name), 'w') as file:
            file.write(json.dumps(data, indent=4,sort_keys=True,ensure_ascii=False))

call_crawler = persist_crawler(file_name)
