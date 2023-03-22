from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import csv

bw = webdriver.Firefox(executable_path="./geckodriver")
bw.get("https://suap.iff.edu.br")
bw.maximize_window()
usr = bw.find_element_by_id("id_username")
pwd = bw.find_element_by_id("id_password")
submit = bw.find_element_by_xpath("//input[@value='Acessar']")

usr.send_keys("2163204")
pwd.send_keys("Thi@g0rinu")

submit.click()

 
csv_reader = csv.reader(open("palestra_pnld.csv"), delimiter=",")

count = 0
for row in csv_reader:
    count += 1
    if count <= 1:
        continue

    print(row)
    # import pdb; pdb.set_trace()
    nome = row[0]
    tipo_evento = "do Seminário"
    papel = row[1]
    doc = row[2]
    tipo_doc = row[3]
    evento = "Sustentabilidade Ambiental em Foco"
    horas = "40"
    dia = "13"
    mes = "Maio"
    ano = "2021"
    data_ini = "06"
    data_fim = "27 de Abril de 2021"
    data_atual = "%s de %s de %s"% ("08", "Junho", "2021")


    clone_url = "https://suap.iff.edu.br/documento_eletronico/clonar_documento/250436/"
    bw.get(clone_url)
    setor_wg = bw.find_element_by_id("id_setor_dono")
    sel = Select(setor_wg)
    sel.select_by_visible_text("DPEICCG")

    bw.find_element_by_id("id_assunto").send_keys("Certificado de %s - %s %s"%(nome, tipo_evento, evento))
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
    txt = bw.find_element_by_xpath("//span[contains(text(),'{nome}')]").get_attribute("innerHTML")

    txt = txt.replace("{nome}", nome)
    txt = txt.replace("{doc}", doc)
    txt = txt.replace("{tipo_doc}", tipo_doc)
    txt = txt.replace("{papel}", papel)
    txt = txt.replace("{tipo_evento}", tipo_evento)
    txt = txt.replace("{evento}", evento)
    txt = txt.replace("{horas}", horas)
    txt = txt.replace("{data_ini}", data_ini)
    txt = txt.replace("{data_fim}", data_fim)
    # txt = txt.replace("{dia}", dia)
    # txt = txt.replace("{mes}", mes)
    # txt = txt.replace("{ano}", ano)
    # import pdb; pdb.set_trace()
    time.sleep(2)
    span = bw.find_element_by_xpath("//span[contains(text(),'{nome}')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span, txt)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    txt = span_data.get_attribute("innerHTML")
    txt = txt.replace("{data}", data_atual)
    time.sleep(2)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'CAMPOS DOS GOYTA')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span_data, txt)

    bw.switch_to.parent_frame()
    bw.find_element_by_name("_salvar_e_visualizar").click()
    # import pdb; pdb.set_trace()
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
    






