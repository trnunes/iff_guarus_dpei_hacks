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

errors = []
csv_reader = csv.reader(open("conepe_presencas_portador.csv"), delimiter=",")
cadastros = []
count = 0
for row in csv_reader:
    count += 1
    if count <= 1:
        continue

    print(row)
    # import pdb; pdb.
    cadastros.append(row)
    

course = "Dos and Don'ts in a job interview"
user = "Fulano da silva"
codigo_certificado = "2021"
browser = webdriver.Firefox(executable_path="./geckodriver")
browser.get("http://conepe.guarus.iff.edu.br/admins/sign_in")
browser.maximize_window()
time.sleep(2)
password = browser.find_element("id","admin_password")
login = browser.find_element("id",'admin_login')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
submit = browser.find_element("xpath", "//input[@value='Entrar']")
login.send_keys("admin@admin.com")
password.send_keys("!@#conepe1234")

submit.click()
n_iter = False
n_iter_ex = False
for i, c in enumerate(cadastros):

    course = c[4]
    user = c[1].upper().strip()
    cod_cert = "20212%d"%i 
    c.append(cod_cert)
    print("CADASTRANDO: ", c)
    print("ERROS: ", errors)
    try:
        browser.get("http://conepe.guarus.iff.edu.br/admin/minicursos_user/new")
        elem = browser.find_element("xpath", "//div[@data-input-for='minicursos_user_user_id']/input")
        elem.send_keys(user)
        time.sleep(2)
        elem.send_keys(Keys.ARROW_DOWN)
        elem.send_keys(Keys.ENTER)
        elem = browser.find_element("xpath", "//div[@data-input-for='minicursos_user_minicurso_id']/input")
        elem.send_keys(course)
        time.sleep(2)
        elem.send_keys(Keys.ARROW_DOWN)
        elem.send_keys(Keys.ENTER)
        elem = browser.find_element("xpath", "//input[@type='checkbox']")
        elem.click()
        cod_input = browser.find_element("id","minicursos_user_cod_certificado")
        cod_input.send_keys(cod_cert)
        elem = browser.find_element("xpath", "//button[@name='_save']")
        # if not n_iter: import pdb;pdb.set_trace()
        elem.click()
        time.sleep(1)
    except:
        
        # if not n_iter_ex: import pdb;pdb.set_trace()
        errors.append(c)
    try:
        if not n_iter: import pdb;pdb.set_trace()
        "Usuário criado sem sucesso"
        browser.find_element("xpath", "//h1[contains(.,'something went wrong')]")
        # if not n_iter_ex: import pdb;pdb.set_trace()
        errors.append(c)
    except:
        pass
        

error_string = "Não foi possível cadastrar os participantes abaixo;\n"
for e in errors:
    error_string += "%s, %s, %s,\n"%(e[0], e[1], e[2])
import pdb;pdb.set_trace()
open("error_minicurso_2_%s.csv"%course, 'w').write(error_string)

