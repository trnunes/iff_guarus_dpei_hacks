from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

bw = webdriver.Firefox(executable_path="./geckodriver")


bw.get("https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login")
bw.get("https://busca.inpi.gov.br/pePI/jsp/patentes/PatenteSearchBasico.jsp")
bw.maximize_window()
num_pedido = bw.find_element_by_xpath("//input[@name='NumPedido']")
num_pedido.send_keys("PI 0608671-3")
btn = bw.find_element_by_xpath("//value[@type=' pesquisar » ']")
btn.click()
btn.click()
# submit = bw.find_element_by_xpath("//input[@value='Acessar']")

# bw.request('POST', 'https://busca.inpi.gov.br/pePI/servlet/PatenteServletController', data={"NumPedido": "PI 0608671-3"})



bw.maximize_window()


