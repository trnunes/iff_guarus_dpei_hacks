import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import locale
import datetime
import csv
import getpass
import os
import re
import shutil

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

bw = webdriver.Firefox(executable_path="./geckodriver", firefox_profile=fp)


bw.get("https://suap.iff.edu.br")
bw.maximize_window()
usr = bw.find_element("id", "id_username")
pwd = bw.find_element("id", "id_password")
submit = bw.find_element("xpath", "//input[@value='Acessar']")

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

modelo = "" 


headers = []

for index, row in enumerate(csv_reader):
    
    if index == 0:
        if "Modelo" in row[0]:
            modelo = row[1]
        continue
    
    if index == 1:
        tipo = row[1]
        continue
    
    if index == 2:
        headers = row
        
        continue

    print(row)
    # import pdb; pdb.set_trace()
    
    
    clone_url = modelo.replace( "editar_documento", "clonar_documento")        
    
        
    
    bw.get(clone_url)
    time.sleep(1)
    setor_wg = bw.find_element("id", "id_setor_dono")
    sel = Select(setor_wg)
    sel.select_by_visible_text("DPEICCG")

    setor_wg = bw.find_element("id", "id_nivel_acesso")
    sel = Select(setor_wg)
    time.sleep(1)
    # sel.select_by_visible_text("Restrito")
    # if not n_iter: import pdb; pdb.set_trace()
    
    doc_title = tipo + " de " + " " + row[0] + " CONEPE 2023"
    bw.find_element("id", "id_assunto").send_keys(doc_title)
    time.sleep(2)
    bw.find_element("xpath", "//input[@value='Salvar']").click()

    bw.get(bw.find_element("xpath", "//a[contains(@href,'editar_documento')]").get_attribute("href"))


    achei = False
    while not achei:
        try:
            bw.switch_to.frame( bw.find_element(By.TAG_NAME, "iframe"))
            achei = True
        except:
            print("aguardando iframe aparecer")

    
    time.sleep(2)
    txt = bw.find_element(By.CLASS_NAME, "corpo").get_attribute("innerHTML")

    nome = ativ = ""
    for index, h in enumerate(headers):
        value = row[index].strip().upper()
        if  h.lower() in ["nome", "coordenador"]:
            nome = value
        
        if h.lower() in ["atividade", "trabalho"]:
            ativ = value
        
        txt = txt.replace("{%s}"%h.strip(), value)
        # import pdb; pdb.set_trace()
    txt = txt.replace("{data}", data)
    time.sleep(2)
    
    span = bw.find_element(By.CLASS_NAME, "corpo")
        
    

    bw.execute_script("arguments[0].innerHTML=arguments[1]", span, txt)

    bw.switch_to.parent_frame()
    bw.find_element("name", "_salvar_e_visualizar").click()
    if n_iter == 2:
        print("\nDeseja assinar e gerar o próximo? \n1-sim e não perguntar novamente \n2-sim e confirmar o próximo \n3-não")
        n_iter = int(input())
    if n_iter == 3:
        bw.close()
        exit()
    time.sleep(2)
    bw.get(bw.find_element("xpath", "//a[contains(@href,'concluir_documento')]").get_attribute("href"))
    bw.get(bw.find_element("xpath", "//a[contains(@href,'assinar_documento')]").get_attribute("href"))
    bw.find_element("name", "geradoridentificadordocumento_form").click()
    # time.sleep(2)
    sel = Select(bw.find_element("id", "id_1-papel"))

    sel.select_by_visible_text("DIRETOR(A) - CD4 - DPEICCG")
    bw.find_element("id", "id_1-senha").send_keys(password)


    bw.find_element("name", "assinardocumento_form").click()
    link_to_pdf = bw.find_element("xpath", "//a[contains(@href,'paisagem')]").get_attribute("href")
    bw.get(link_to_pdf)
    wait = WebDriverWait(bw, 60)  # waits for 60 seconds

    continue_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Continuar']")))
    download_dir = "/home/thiago/Downloads"
    destination_dir = "./certificados_e_cartas_geradas"

    # List files matching the pattern "Documento(x)"
    time.sleep(4)
    matching_files = [f for f in os.listdir(download_dir) if re.match(r'Documento\(\d+\)', f)]

    # Sort them based on the sequence number "x" to get the latest one
    matching_files.sort(key=lambda f: int(re.search(r'\((\d+)\)', f).group(1)))

    # Take the latest file
    latest_file = matching_files[-1]

    # Move the latest file to the desired directory
    source_path = os.path.join(download_dir, latest_file)
    destination_path = os.path.join(destination_dir, "%s_%s.pdf" % (nome, ativ.replace("\\", "_")))
    
    shutil.move(source_path, destination_path)


    # bw.find_element("id", "download").click()
    bw.find_element("xpath", "//a[text()='Continuar']").click()
    # import pdb; pdb.set_trace()
    time.sleep(2)
    
    # import pdb; pdb.set_trace()
    # if count == 3: import pdb; pdb.set_trace()