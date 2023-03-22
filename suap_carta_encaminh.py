from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import locale
import datetime
import csv

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
data = datetime.datetime.now().strftime('%d de %B de %Y')

bw = webdriver.Firefox(executable_path="./geckodriver")
bw.get("https://suap.iff.edu.br")
bw.maximize_window()
usr = bw.find_element_by_id("id_username")
pwd = bw.find_element_by_id("id_password")
submit = bw.find_element_by_xpath("//input[@value='Acessar']")

usr.send_keys("2163204")
pwd.send_keys("Thi@g0rinu")

submit.click()

 
csv_reader = csv.reader(open("conepe_apresentacoes_culturais.csv"), delimiter=",")

count = 0
n_iter = False
text = """

"""

for row in csv_reader:
    count += 1
    
    if count <= 1:
        modelo = row[1]
        continue
    
    if count == 2:
        continue

    print(row)
    # import pdb; pdb.set_trace()
    cpf = None
    
    nome = row[0]    
    cpf = row[1]
    papel = row[2]
    particip = row[3] 
    ativ = row[4]
    
    data_ativ = row[5]
    data_inicio = row[6]
    data_fim = row[7]
    horas = row[8]
    evento = row[9] 
    

    clone_url = "https://suap.iff.edu.br/documento_eletronico/clonar_documento/277630/"
    bw.get(clone_url)
    setor_wg = bw.find_element_by_id("id_setor_dono")
    sel = Select(setor_wg)
    sel.select_by_visible_text("DPEICCG")

    setor_wg = bw.find_element_by_id("id_nivel_acesso")
    sel = Select(setor_wg)
    time.sleep(1)
    sel.select_by_visible_text("Restrito")
    # if not n_iter: import pdb; pdb.set_trace()
    

    bw.find_element_by_id("id_assunto").send_keys("Certificado de %s - %s '%s'"%(nome, papel,ativ))
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
    # txt = bw.find_element_by_xpath("//span[contains(text(),'{nome}')]").get_attribute("innerHTML")
    txt = modelo
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

    
    
    
    
    # txt = txt.replace("{dia}", dia)
    # txt = txt.replace("{mes}", mes)
    # txt = txt.replace("{ano}", ano)
    # import pdb; pdb.set_trace()
    time.sleep(2)
    span = bw.find_element_by_xpath("//span[contains(text(),'{nome}')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span, txt)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    txt = span_data.get_attribute("innerHTML")
    txt = txt.replace("{data}", data)
    time.sleep(2)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span_data, txt)

    bw.switch_to.parent_frame()
    bw.find_element_by_name("_salvar_e_visualizar").click()
    if not n_iter: import pdb; pdb.set_trace()
    time.sleep(2)
    bw.get(bw.find_element_by_xpath("//a[contains(@href,'concluir_documento')]").get_attribute("href"))
    bw.get(bw.find_element_by_xpath("//a[contains(@href,'assinar_documento')]").get_attribute("href"))
    bw.find_element_by_name("geradoridentificadordocumento_form").click()
    
    sel = Select(bw.find_element_by_id("id_1-papel"))
    sel.select_by_visible_text("DIRETOR - CD4 - DPEICCG")
    bw.find_element_by_id("id_1-senha").send_keys("Thi@g0rinu")


    bw.find_element_by_name("assinardocumento_form").click()
    
    bw.get(bw.find_element_by_xpath("//a[contains(@href,'paisagem')]").get_attribute("href"))
    bw.find_element_by_id("download").click()
    
    time.sleep(2)
    
    # import pdb; pdb.set_trace()
    # if count == 3: import pdb; pdb.set_trace()
    






