import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import locale
import datetime
import csv
import getpass

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
data = datetime.datetime.now().strftime('%d de %B de %Y')
mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "/home/aafanasiev/Downloads")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
fp.set_preference("pdfjs.disabled", True)

bw = webdriver.Firefox(executable_path="./geckodriver.exe", firefox_profile=fp)


bw.get("https://suap.iff.edu.br")
bw.maximize_window()
usr = bw.find_element_by_id("id_username")
pwd = bw.find_element_by_id("id_password")
submit = bw.find_element_by_xpath("//input[@value='Acessar']")

print("Informe a matrícula do suap: ")
login = input()
password = getpass.getpass()


usr.send_keys(login)
pwd.send_keys(password)

submit.click()
selenium_cookies = bw.get_cookies()
session = requests.session()

for cookie in selenium_cookies:
    session.cookies.set(cookie["name"], cookie["value"])

file_path = "./dados_para_gerar.csv"
csv_reader = csv.reader(open(file_path, encoding="utf8"), delimiter=",")

count = 0
n_iter = 2

certs_conepe_apres_orais = """
Certificamos que {nome}, inscrito(a) no CPF {cpf}, participou como {papel} das {tipo_atividade} da "{atividade}", em {data_atividade}, no {evento}, ocorrido de {data_inicio} até {data_fim}, pelo INSTITUTO FEDERAL FLUMINENSE CAMPUS CAMPOS GUARUS, com carga horária de {horas} horas.
"""

certs_conepe = """
Certificamos que {nome}, inscrito(a) no CPF {cpf}, participou como {papel} {tipo_atividade} "{atividade}", em {data_atividade}, no {evento}, ocorrido de {data_inicio} até {data_fim}, pelo INSTITUTO FEDERAL FLUMINENSE CAMPUS CAMPOS GUARUS, com carga horária de {horas} horas.
"""
cert_lauanna = """
    Certificamos que {nome}, inscrito(a) no CPF {cpf}, participou como {papel} no {evento}, ocorrido de {data_inicio} até {data_fim} pelo INSTITUTO FEDERAL FLUMINENSE CAMPUS CAMPOS GUARUS.
"""

cert_jinecult = """
Certificamos que {nome} participou da {papel} da {evento}, ocorrido de {data_inicio} até {data_fim} pela UNIVERSIDADE ESTADUAL DO NORTE FLUMINENSE DARCY RIBEIRO, em parceria com o INSTITUTO FEDERAL FLUMINENSE CAMPUS CAMPOS GUARUS, com carga horária de {horas}.
"""

cert_diego = """
Certificamos que Diego da Silva Sales, portador do documento 098.239.317-20, participou do
I simpósio multidisciplinar sobre corrida de rua, realizado nos dias 03, 10, 17 e 24 de junho e 01 de julho de 2020, no INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA
FLUMINENSE CAMPUS CAMPOS GUARUS, na cidade de Campos dos Goytacazes/RJ, com carga horária de 40 horas.
	
"""
print("\nO que você deseja emitir? \n1-Carta de Encaminhamento \n2-Certificado \n3-Declaração\n4-Encerrar")
doc_type = int(input())
if doc_type == 4:
    bw.close()
    exit()
for row in csv_reader:
    count += 1
    
    if count <= 1:
        modelo = row[1]
        continue
    
    if count == 2:
        continue

    print(row)
    # import pdb; pdb.set_trace()
    cpf=""
    nome=""
    curso=""
    periodo=""
    matricula=""
    papel=""
    particip=""
    ativ=""
    data_ativ=""
    data_inicio=""
    data_fim=""
    horas=""
    evento=""
    clone_url = "https://suap.iff.edu.br/documento_eletronico/clonar_documento/277630/"
    concedente = ""
    doc_title = ""
    if doc_type == 1:
        nome = row[0].strip()
        matricula = row[1].strip()
        curso = row[2].strip()
        periodo = row[3].strip()
        concedente = row[4].strip()
        clone_url = "https://suap.iff.edu.br/documento_eletronico/clonar_documento/355454/"
        doc_title = "Carta de Encaminhamento de %s (%s) para '%s'"%(nome, matricula,concedente)
        modelo=""
    else:
        cpf = None

        nome = row[0].strip()    
        cpf = row[1].strip()
        papel = row[2].strip()
        particip = row[3].strip() 
        ativ = row[4].strip()

        data_ativ = row[5].strip()
        data_inicio = row[6].strip()
        data_fim = row[7].strip()
        horas = row[8].strip()
        evento = row[9].strip()
        doc_title = "Certificado de %s - %s '%s'"%(nome, papel,ativ)
    

    
    bw.get(clone_url)
    setor_wg = bw.find_element_by_id("id_setor_dono")
    sel = Select(setor_wg)
    sel.select_by_visible_text("DPEICCG")

    setor_wg = bw.find_element_by_id("id_nivel_acesso")
    sel = Select(setor_wg)
    time.sleep(1)
    sel.select_by_visible_text("Restrito")
    # if not n_iter: import pdb; pdb.set_trace()
    

    bw.find_element_by_id("id_assunto").send_keys(doc_title)
    time.sleep(2)
    bw.find_element_by_name("_save").click()

    bw.get(bw.find_element_by_xpath("//a[contains(@href,'editar_documento')]").get_attribute("href"))


    achei = False
    while not achei:
        try:
            bw.switch_to.frame( bw.find_element_by_tag_name("iframe"))
            achei = True
        except:
            print("aguardando iframe aparecer")

    
    time.sleep(2)
    if modelo:
        txt = modelo
    else:
        txt = bw.find_element_by_class_name("corpo").get_attribute("innerHTML")

    # import pdb; pdb.set_trace()
    txt = txt.replace("{nome}", nome.upper())
    if not cpf:
        txt = txt.replace(", inscrito(a) no CPF {cpf}, ", " ")
    txt = txt.replace("{cpf}", cpf.strip())
    txt = txt.replace("{papel}", papel.strip())
    txt = txt.replace("{tipo_atividade}", particip.strip())
    txt = txt.replace("{atividade}", ativ.strip())
    txt = txt.replace("{evento}", evento.strip())
    txt = txt.replace("{data_atividade}", data_ativ.strip())
    txt = txt.replace("{data_inicio}", data_inicio.strip())
    txt = txt.replace("{data_fim}", data_fim.strip())
    txt = txt.replace("{horas}", horas.strip())
    txt = txt.replace("{matricula}", matricula)
    txt = txt.replace("{periodo}", periodo)
    txt = txt.replace("{concedente}", concedente)
    txt = txt.replace("{curso}", curso)

    
    
    
    
    # txt = txt.replace("{dia}", dia)
    # txt = txt.replace("{mes}", mes)
    # txt = txt.replace("{ano}", ano)
    # import pdb; pdb.set_trace()
    time.sleep(2)
    
    span = bw.find_element_by_class_name("corpo")
        
    

    bw.execute_script("arguments[0].innerHTML=arguments[1]", span, txt)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    txt = span_data.get_attribute("innerHTML")
    txt = txt.replace("{data}", data)
    time.sleep(2)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span_data, txt)

    bw.switch_to.parent_frame()
    bw.find_element_by_name("_salvar_e_visualizar").click()
    if n_iter == 2:
        print("\nDeseja assinar e gerar o próximo? \n1-sim e não perguntar novamente \n2-sim e confirmar o próximo \n3-não")
        n_iter = int(input())
    if n_iter == 3:
        bw.close()
        exit()
    time.sleep(2)
    bw.get(bw.find_element_by_xpath("//a[contains(@href,'concluir_documento')]").get_attribute("href"))
    bw.get(bw.find_element_by_xpath("//a[contains(@href,'assinar_documento')]").get_attribute("href"))
    bw.find_element_by_name("geradoridentificadordocumento_form").click()
    # time.sleep(2)
    sel = Select(bw.find_element_by_id("id_1-papel"))

    sel.select_by_visible_text("DIRETOR - CD0004 - DPEICCG")
    bw.find_element_by_id("id_1-senha").send_keys(password)


    bw.find_element_by_name("assinardocumento_form").click()
    link_to_pdf = bw.find_element_by_xpath("//a[contains(@href,'paisagem')]").get_attribute("href")
    pdf_response = session.get(link_to_pdf)
    with open("./certificados_e_cartas_geradas/%s.pdf"%nome, 'wb') as f:
        f.write(pdf_response.content)

    # bw.find_element_by_id("download").click()
    
    time.sleep(2)
    
    # import pdb; pdb.set_trace()
    # if count == 3: import pdb; pdb.set_trace()
    






