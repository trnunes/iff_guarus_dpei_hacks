from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, WebDriverException
from selenium.webdriver.common.keys import Keys
import ctypes
import easygui
import sys

import tkinter as tk



easygui.msgbox("This is a message!", title="simple gui")
bw = webdriver.Firefox(executable_path="./geckodriver")

while(True):
    try:
        bw.get("https://inscricao.capes.gov.br/")
        

    except WebDriverException as error: 
        print(error)





