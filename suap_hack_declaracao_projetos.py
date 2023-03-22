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

 
csv_reader = csv.reader(open("declaracoes_josi_projetos.csv"), delimiter=",")

count = 0
n_iter = False
for row in csv_reader:
    count += 1
    if count <= 1:
        continue

    print(row)
    # import pdb; pdb.set_trace()
    docente = row[0]
    matricula = row[1]
    papel = row[2]
    tipo = row[3]
    projeto = row[4]
    edital = row[5]
    ini = row[6]
    fim = row[7]
    
    dia = "12"
    mes = "Julho"
    ano = "2021"
    data = "%s de %s de %s"%(dia, mes, ano)


    clone_url = "https://suap.iff.edu.br/documento_eletronico/clonar_documento/247769/"
    bw.get(clone_url)
    setor_wg = bw.find_element_by_id("id_setor_dono")
    sel = Select(setor_wg)
    sel.select_by_visible_text("DPEICCG")

    bw.find_element_by_id("id_assunto").send_keys("Declaração de %s (%s do Projeto de %s \"%s\")"%(papel, docente, tipo, projeto))

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

    txt = txt.replace("{nome}", docente)
    txt = txt.replace("{mat}", matricula)
    txt = txt.replace("{tipo_projeto}", tipo)
    txt = txt.replace("{papel}", papel)
    txt = txt.replace("{projeto}", projeto)
    txt = txt.replace("{edital}", edital)
    txt = txt.replace("{data_inicio}", ini)
    txt = txt.replace("{data_fim}", fim)
    txt = txt.replace("{data}", data)
    # import pdb; pdb.set_trace()
    time.sleep(2)
    span = bw.find_element_by_xpath("//span[contains(text(),'{nome}')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span, txt)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'Campos dos')]")
    txt = span_data.get_attribute("innerHTML")
    txt = txt.replace("{data}", data)
    time.sleep(2)
    span_data = bw.find_element_by_xpath("//span[contains(text(),'Campos dos')]")
    bw.execute_script("arguments[0].innerHTML=arguments[1]", span_data, txt)

    bw.switch_to.parent_frame()
    bw.find_element_by_name("_salvar_e_visualizar").click()
    if not n_iter: import pdb; pdb.set_trace()
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
    
    
    # if count == 3: import pdb; pdb.set_trace()
    






