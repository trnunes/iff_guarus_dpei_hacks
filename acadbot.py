#------Passo-a-Passo para Instalação no Ubuntu-----------

# 1 - certifique-se de que o python3 está instalado: python3 --version

# 2 - certifique-se de que o pip3 está instalado: pip3 --version

# 3 - Instale o gerenciador de ambientes virtuais: pip3 install --user virtualenv

# 4 - Crie um ambiente virtual: virtualenv bot_venv

# 5 - Ative o ambiente criado: source bot_venv/bin/activate

# 6 - pelo terminal navegue para a pasta bot_academico

# 7 - instale os frameworks: pip install -r acad_requirements.txt 

# 8 - Abra o arquivo acadbot.py e substitua as linhas abaixo, ao final, colocando o seu login e senha do acadêmico:
#   -   login = "meu_login"
#   -   senha = "minha_senha"

# 9 - Execute o script para lançar as aulas:

#   python acadbot.py exemplos/planej_aulas_ma_proeja.csv

# Obs. Para montagem da planilha em csv, veja os exemplos na pasta exemplos/

# 10 - Para lançar faltas para todos os alunos execute com o parâmetro -f

#   python acadbot.py exemplos/planej_aulas_ma_proeja.csv -f

# 11 - Para lançar notas basta passar o arquivo com as notas e o arquivo contendo as matrículas dos alunos:

#  python acadbot.py exemplos/Notas_MA.csv exemplos/Banco_MA.csv

#   Obs. Para formatar a planilha de notas e o banco da turma, veja as planilhas de exemplo. O código da avaliação pode ser encontrado após a sua criação no acadêmico, como um parâmetro na URL do link "lançar notas".

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import datetime
from datetime import date
import sys
import codecs
import re
import unidecode


class ProfessorBot:
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path="./geckodriver")        
        
    def login(self, str_login, str_senha):
        self.browser.get("http://www.academico.iff.edu.br")
        self.browser.find_element_by_partial_link_text("PROFESSOR").click()
        self.browser.find_element_by_xpath("//input[@name='LOGIN']").send_keys(str_login)
        self.browser.find_element_by_xpath("//input[@name='SENHA']").send_keys(str_senha)
        self.browser.find_element_by_xpath("//input[@name='Submit']").click()

    def acessa_meus_diarios(self):
        achei = False
        while not achei:
            try:
                
                link = self.browser.find_element_by_partial_link_text("Meus") # Meus Diarios
                achei = True
            except:
                pass
        link.click()
        # tempo para aparecer os diários
        time.sleep(2)

    def acessa_etapa(self, etapa, is_frequencia):    
        link_diario = None    
        achei = False
        if is_frequencia:
            manutencao_pauta = "3066"
        else:
            manutencao_pauta = "3068"
        
        while not achei:
            try:
                
                link_diario = self.browser.find_element_by_xpath("//a[contains(@href,'"+ manutencao_pauta+"') and contains(@href,'"+ hash_db['diario'].strip() + "') and contains(@href, '"+ etapa.strip()+"')]")

                achei = True
            except:
                pass            
        link_diario.click()

    def cadastra_aulas(self, lanca_faltas=False):

        
        erros = []
        acessa_diarios_page = True
        for conteudo_etapa in hash_db['etapas']:
            self.acessa_meus_diarios()

            self.acessa_etapa(conteudo_etapa.pop(0), True)

            for data_conteudo in conteudo_etapa:
                texto_botao = "Inserir"
                try:
                    self.find_editar(data_conteudo)
                    texto_botao = "Salvar"
                    lanca_faltas = False

                except:
                    print('Aula ainda não cadastrada: ', data_conteudo, '. Fazendo novo cadastro!')
                
                try:
                    e = self.browser.find_element_by_xpath("//input[@name='DT_AULA_MINISTRADA']")
                    e.clear()
                    e.send_keys(data_conteudo[0])
                    #
                    e = self.browser.find_element_by_xpath("//input[@name='HORARIO_INI']")
                    e.clear()
                    e.send_keys(hash_db['hora_inicio'])
                    #
                    e = self.browser.find_element_by_xpath("//input[@name='HORARIO_FIN']")
                    e.clear()
                    e.send_keys(hash_db['hora_fim'])
                    #
                    e = self.browser.find_element_by_xpath("//input[@name='N_AULAS']")
                    e.clear()
                    e.send_keys(hash_db['qtd_aulas'])

                    faltas_inputs = self.browser.find_elements_by_xpath("//input[contains(@name,'N_FALTAS_')]")
                    if lanca_faltas:
                        for falta_input in faltas_inputs:
                            falta_input.send_keys(Keys.BACKSPACE*10)
                            falta_input.send_keys(hash_db['qtd_aulas'])
                    
                    e = self.browser.find_element_by_xpath("//textarea[@name='CONTEUDO']")
                    e.clear()
                    e.send_keys(data_conteudo[1])
                    #

                    e = self.browser.find_element_by_xpath("//input[@value='%s']" % texto_botao)
                    e.click()
                    #
                except:

                    erros.append(data_conteudo)

                time.sleep(2)
        if len(erros):
        
            print("-------------ERRO AO CADASTRAR AS AULAS ABAIXO--------------")
            for erro in erros:
                print(erro, "\n")
        
            
    def cadastra_notas(self, arquivo_path):
        print("------CADASTRANDO NOTAS---------")
        
        
        erros = []

        link_template = "https://academico.iff.edu.br/qacademico/index.asp?t=3068&ACAO=LANCAR&COD_PAUTA=%s&COD_AVALIACAO=%s&N_ETAPA=%s"
        self.browser.get(link_template % (hash_db['diario'], hash_db['avaliacao'], hash_db['etapa']))
        print("LINK AVALIAÇÃO: ", link_template % (hash_db['diario'], hash_db['avaliacao'], hash_db['etapa']))
        matriculas_list = []

        for matricula_nome_nota in hash_db['notas']:

                try:
                    print("Tentando Cadastrar ", matricula_nome_nota[1], " com: ", matricula_nome_nota[2])
                    input_nota_aluno = self.browser.find_element_by_xpath("//a[text()='%s']/../..//input[contains(@name, 'NOTA')]" % matricula_nome_nota[0])
                    input_nota_aluno.send_keys(Keys.BACKSPACE*10)
                    input_nota_aluno.send_keys(matricula_nome_nota[2])
                    
                
                except:                    
                    erros.append("ERRO: Aluno %s não foi encontrado!" % matricula_nome_nota)
        
        self.browser.find_element_by_xpath("//input[@value='Salvar']").click()
            
        for erro in erros:
            print(erro)

    def find_editar(self, data_conteudo):

        mes_ano = data_conteudo[0].split("/")[1] + "/" + data_conteudo[0].split("/")[2]
        if mes_ano[0] == '0': mes_ano = mes_ano[1:len(mes_ano)]
        
        dia = data_conteudo[0].split("/")[0]
        if dia[0] == "0": dia = dia[1::len(dia)]
        dados_aula = [mes_ano, dia, hash_db['hora_inicio']]
        m = []
        #import pdb; pdb.set_trace()
        div = self.browser.find_element_by_id("div_secao_central")
        table = div.find_element_by_xpath("./table")
        trs = table.find_elements_by_xpath("./tbody/tr")        
        for i in range(len(trs)-1): 
            columns = []
            for cl in trs[i].find_elements_by_xpath("./td"):
                colspan = cl.get_attribute("colspan")

                if not colspan: colspan = 1
                for i in range(int(colspan)):
                    columns.append(cl)
            m.append(columns)
        #import pdb; pdb.set_trace()
        for j in range(len(m[0])):
            texts = []
            for i in range(len(m)):
                texts.append(m[i][j].text)
            print(texts)
            print(dados_aula)
            contained = all(t in texts for t in dados_aula)
            if contained:
         #       import pdb; pdb.set_trace()
                botao_editar = m[5][j].find_element_by_xpath("./div/a[contains(@href, 'ACAO=EDITAR')]")
                break

        
        botao_editar.click()

        
        
    def libera_conexao(self):
        self.browser.close()

def leia_aulas(arquivo_path):
    with codecs.open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as diario_csv:
        linha_diario_list = diario_csv.readlines()
    #removendo primeira linha (cabeçalho da planilha)
    linha_diario_list.pop(0)
    #encontrando o número do diário
    linha_diario = linha_diario_list.pop(0)

    diario_id = linha_diario.split(",")[1].replace('\n', "")    
    print("Número do Diário: ", diario_id)
    hash_db['diario'] = diario_id
    linha_diario = linha_diario_list.pop(0)
    print("Linha: ", linha_diario)

    # recuperando numero de aulas, hora início e hora fim
    linha_diario = linha_diario_list.pop(0)
    print("Linha: ", linha_diario)
    numero_aulas = linha_diario.split(",")[0]
    hash_db['qtd_aulas'] = numero_aulas
    hora_inicio = linha_diario.split(",")[1]
    hash_db['hora_inicio'] = hora_inicio
    hora_fim = linha_diario.split(",")[2]
    hash_db['hora_fim'] = hora_fim
    print("Número de Aulas: ", numero_aulas)
    print("Hora Início: ", hora_inicio)
    print("Hora Fim: ", hora_fim)

    linha_diario = linha_diario_list.pop(0)
    print("Linha: ", linha_diario)
    etapa = linha_diario.split(",")[1].replace('\n', "")

    hash_db['etapas'] = []
    aulas_etapa = [etapa]
    hash_db['etapas'].append(aulas_etapa)
    print("Etapa: ", etapa)
#    
    #Acessando primeira etapa
    for linha_diario in linha_diario_list:
        print(linha_diario)

        if 'imestre' in linha_diario.split(",")[0] or 'tapa' in linha_diario.split(",")[0]:

            etapa = linha_diario.split(",")[1].replace('\n', "")

            aulas_etapa = [etapa]
            hash_db['etapas'].append(aulas_etapa)
 #           

            continue
        conteudo = re.findall(r'"([^"]*)"', linha_diario)
        if not conteudo and len(linha_diario.split(",")) > 1:          conteudo = linha_diario.split(",")[1].replace('\n', "")
        sdata = linha_diario.split(",")[0]
        print(sdata, ": ", conteudo)
        
        aulas_etapa.append([sdata, conteudo])

def leia_notas(arquivo_path, base_lines):
    print("------CADASTRANDO NOTAS---------")
        
    with codecs.open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as diario_csv:
        notas_list = diario_csv.readlines()
        notas_list.pop(0)
        linha_diario = notas_list.pop(0)
        id_diario = linha_diario.split(",")[1].replace('\n', "")
        hash_db['diario'] = id_diario
        print("Diário: ", id_diario)

        linha_diario = notas_list.pop(0)
        print(linha_diario)
        etapa = linha_diario.split(",")[1].replace('\n', "")
        hash_db['etapa'] = etapa
        print("Etapa: ", etapa)

        linha_diario = notas_list.pop(0)
        print(linha_diario)
        cod_avaliacao = linha_diario.split(",")[1].replace('\n', "")
        hash_db['avaliacao'] = cod_avaliacao
        
        print("Código Avaliação:", cod_avaliacao)
        notas_list.pop(0)        
        print("notas list", notas_list)
        hash_db['notas'] = []

        for tupla_nota in notas_list:
            print("Tupla da nota", tupla_nota)
            if tupla_nota.find('"') >= 0:
                nome_aluno_str = re.findall(r'\"([^\\].*)\"',tupla_nota)[0].lower()
            else:
                nome_aluno_str = tupla_nota.split(",")[0].lower()
#            
            nomes_list = [nome_aluno_str]
            if nome_aluno_str.find(" e ") >= 0:
                nomes_list = nome_aluno_str.split(" e ")
            if nome_aluno_str.find(";") >= 0:
                nomes_list = nome_aluno_str.split(";")
            if nome_aluno_str.find(",") >= 0:
                nomes_list = nome_aluno_str.split(",")

            nota_aluno = re.findall(r'\d+(?:,|.\d+)?',tupla_nota)
            if not nota_aluno: nota_aluno = ["0"]
            print(nota_aluno)
            nota_aluno = nota_aluno[0].replace(".", ",")
            matricula = ""
            for parte_nome_aluno in nomes_list:
                matricula = achar_matricula(base_lines, parte_nome_aluno.strip())

                print("Aluno: ", parte_nome_aluno.strip().title(), " Matrícula: ", matricula,"com: ", nota_aluno)
                hash_db['notas'].append([matricula, parte_nome_aluno.strip().title(), nota_aluno])

def achar_matricula(base_lines, nome_snippet):
    nome_snippet = unidecode.unidecode(nome_snippet)
    for line in base_lines:
                
        line = unidecode.unidecode(line.replace('\r', "").replace('\n', ""))
        matricula = line.split(",")[0]
    
        nome_aluno = line.split(",")[-1].lower()

        if nome_snippet == nome_aluno:
            return matricula
        else:
            splitted_nome = unidecode.unidecode(nome_aluno).split(" ")
            contained = all(snippet in splitted_nome for snippet in nome_snippet.split(" "))

            if contained:
                return matricula

    return ""

def lanca_aulas(arquivo, login, senha, lancar_faltas=False):
    bot = ProfessorBot()
    leia_aulas(arquivo)
    bot.login(login, senha)

    bot.cadastra_aulas(lancar_faltas)
    bot.libera_conexao()

def lanca_notas(arquivo, base, login, senha):
    base_lines = []
    with codecs.open(base, 'r', encoding='utf-8', errors='ignore') as arquivo_base:
                base_lines = arquivo_base.readlines()
    leia_notas(arquivo, base_lines)
    bot = ProfessorBot()
    bot.login(login, senha)
    bot.acessa_meus_diarios()
    bot.cadastra_notas(arquivo)
    bot.libera_conexao()    


        

        
if __name__ == "__main__":
    print("args: ", sys.argv)
    if len(sys.argv) < 2:
        print("Informe o caminho do arquivo CSV para lançar aulas ou notas!")
        exit()
    login = "trnunes"
    senha = "thi@g0rinu"
    arquivo = sys.argv[1]
    base = ""
    base_lines = []

    lancar_faltas = False
    for arg in sys.argv[2:len(sys.argv)]:
        if arg.strip() == "-f": lancar_faltas = True
    with open(arquivo, 'r', errors='replace') as diario:
        linhas_contendo_nota = [linha for linha in diario.readlines() if "nota" in linha.lower()]
    print("LANÇAMENTO DE NOTAS: ", linhas_contendo_nota)
    if len(linhas_contendo_nota):
        if len(sys.argv) >= 3:
            base = sys.argv[2]
        
        lanca_notas(arquivo, base, login, senha)
    else:
        lanca_aulas(arquivo, login, senha, lancar_faltas)
