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

browser = webdriver.Firefox(executable_path="../geckodriver")
browser.get("http://conepe.guarus.iff.edu.br/admins/sign_in")
browser.maximize_window()
time.sleep(2)
password = browser.find_element_by_id("admin_password")
login = browser.find_element_by_id('admin_login')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
submit = browser.find_element_by_xpath("//input[@value='Entrar']")
login.send_keys("thiago.nunes@iff.edu.br")
password.send_keys("10203040")
submit.click()
errors = []
for i in range(1, 312):
    url = "http://conepe.guarus.iff.edu.br/admin/work/%d"%str(i)
    
    browser.get(url)
    time.sleep(3)
    try:
        link_pdf = browser.find_element_by_xpath("//a[contains(@href, '.pdf')]")
    except:
        errors.append(url)
    href = link_pdf.get_attribute('href')
    r = requests.get(href, allow_redirects=True)
    title_w = browser.find_element_by_id("work_title")
    title = title_w.get_attribute("value").replace("/", "-") + ".pdf"
    open(title, 'wb').write(r.content)

print("---------------ARQUIVOS COM PROBLEMAS------------")
[print(e) for e in errors]
# final_link = "http://www.conepe.guarus.iff.edu.br/resumos_academicos/270/avaliacoes_finais/novo"
# browser.get(final_link)
# th_nota = browser.find_element_by_xpath("//th[contains(., 'Nota final')]/following-sibling::th")
# nota = float(th_nota.get_attribute("innerHTML"))
# comment = browser.find_element_by_id("avaliacao_final_comentarios")
# text_aprovado = "Seu trabalho foi aprovado"
# text_reprovado = "Trabalho reprovado."
# if nota > 6:
#     print("Trabalho Aprovado")
#     sel = Select(browser.find_element_by_id("avaliacao_final_formato_aprovado"))
#     sel.select_by_visible_text("Banner")
#     comment.send_keys(text_aprovado)
# else:
#     print("Trabalho Reprovado")
#     comment.send_keys(text_reprovado)

# btn_salvar = browser.find_element_by_xpath("//input[@name='commit']")




