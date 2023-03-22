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
import requests
import csv


participantes = [
]

csv_reader = csv.reader(open("credenciamento_conepe_2021.csv"), delimiter=",")
cadastros = []
count = 0
for row in csv_reader:
    count += 1
    if count <= 1:
        continue

    print(row)
    # import pdb; pdb.
    participantes.append(row)

browser = webdriver.Firefox(executable_path="./geckodriver")
browser.get("http://conepe.guarus.iff.edu.br/admins/sign_in")
browser.maximize_window()
time.sleep(2)
password = browser.find_element_by_id("admin_password")
login = browser.find_element_by_id('admin_login')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
submit = browser.find_element_by_xpath("//input[@value='Entrar']")
login.send_keys("thiago.nunes@iff.edu.br")
password.send_keys("Thi@g0rinu")
submit.click()
cadastros = []
emails = []
errors = []
particip_ids = [p[1].replace(".", "").replace("-", "").strip() for p in participantes]
count = 0
for i in range(1, 900):
    url = "http://conepe.guarus.iff.edu.br/admin/user/%d/edit/"%i
    browser.get(url)
    
    try:
        
        cpf = browser.find_element_by_id("user_cpf").get_attribute('value')
        cpf_clean = cpf.replace(".", "").replace("-", "").strip()
        
        email = browser.find_element_by_id("user_email").get_attribute('value')
        email_clean = email.replace(".", "").replace("-", "").strip()
        # import pdb; pdb.set_trace() 
        if cpf_clean in particip_ids or email_clean in particip_ids:
            check_apresentado = browser.find_element_by_id("user_presence")
            count += 1
            print(count)
            if not check_apresentado.get_attribute("checked"):
                print("Cadastrando presença: ", cpf)
                check_apresentado.click()
                save = browser.find_element_by_name("_save")
                # import pdb;pdb.set_trace()
                save.click()
                time.sleep(2)
                if "atualizado sem sucesso" in browser.find_element_by_class_name("alert-danger").get_attribute("innerHTML"):
                    errors.append(cpf)
                else:
                    print("PRESENTE: ", cpf)
                    emails.append(email)
                    cadastros.append(cpf)
            else:
                print("PRESENTE: ", cpf)
                emails.append(email)
                cadastros.append(cpf)
    
            
    except:
        errors.append(url)
        # import pdb; pdb.set_trace() 


cadastrados_str = "CADASTROS,,\n"
for cpf in cadastros:
    cadastrados_str += '"%s"\n'%cpf

open("credenciados.csv", 'w').write(cadastrados_str)
print("Não foi possível cadastrar")
cadastros_clean = [c.replace(".", "").replace("-", "").strip() for c in cadastros]
emails_clean = [e.replace(".", "").replace("-", "").strip() for e in emails]
diff = [t for t in particip_ids if t not in cadastros_clean or t not in emails_clean]
[print(t) for t in diff]
print("-------------ERROS-------------")
[print(e) for e in errors]