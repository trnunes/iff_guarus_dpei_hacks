from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import datetime
from datetime import date
import sys
import os
def csv_to_academico(file, milestone, login, password):
    import csv
    
    student_grades = []
    diary = ""
    task = ""
    type = ""
    date = ""
    with open(file, newline='') as csv_file:
        reader = csv.reader(csv_file)
        student_grades = []
        
        for index, row in enumerate(reader):
            # import pdb;pdb.set_trace()
            if index == 0:
                # import pdb;pdb.set_trace()
                diary = row[0]
                task = row[1]
                type = row[2]
                date = row[3]
                print(row)
                continue
            student_grades.append([row[0], row[1]])
        
    # browser = webdriver.Chrome()
    import pdb;pdb.set_trace()
    data = datetime.datetime.now().strftime('%d de %B de %Y')
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", "/home/aafanasiev/Downloads")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    fp.set_preference("pdfjs.disabled", True)


    browser = webdriver.Firefox(executable_path="./geckodriver", firefox_profile=fp)
    #login    
    erros = []
    try:
        browser.get("http://www.academico.iff.edu.br")

        browser.find_element(by=By.PARTIAL_LINK_TEXT, value="PROFESSOR").click()
        browser.find_element("xpath", "//input[@name='LOGIN']").send_keys(login)
        browser.find_element("xpath", "//input[@name='SENHA']").send_keys(password)
        browser.find_element("xpath", "//input[@name='Submit']").click()

        achei = False
        while not achei:
            try:
                link = browser.find_element(by=By.PARTIAL_LINK_TEXT, value="Meus") # Meus Diarios
                achei = True
            except:
                pass

        link.click()

        # tempo para aparecer os diários
        time.sleep(2)




        link_diario = None    
        achei = False
        manutencao_pauta = "3068"
        while not achei:
            try:
                # import pdb;pdb.set_trace()
                link_diario = browser.find_element("xpath", "//a[contains(@href,'"+ manutencao_pauta+"') and contains(@href,'"+ diary.strip() + "') and contains(@href, '"+ milestone.strip()+"')]")
                
                achei = True
            except:
                pass            

        link_diario.click()

        av_desc = task
        av_type = type
        av_date = data
        try:
            lancar_notas = browser.find_element("xpath", "//td[contains(., '%s')]/following-sibling::td/a[contains(., 'Lançar')]"%av_desc)
        except:
            input = browser.find_element("xpath", "//input[contains(@value, 'Inserir')]")
            input.click()
            sel = Select(browser.find_element("xpath", "//select[contains(@name, 'TIPO')]"))
            desc = browser.find_element("xpath", "//input[contains(@name, 'DESC')]")
            date = browser.find_element("xpath", "//input[contains(@name, 'DT')]")

            sel.select_by_visible_text(av_type)
            desc.send_keys(av_desc)
            date.send_keys(av_date)

            input = browser.find_element("xpath", "//input[contains(@value, 'Inserir')]")
            input.click()

        lancar_notas = browser.find_element("xpath", "//td[contains(., '%s')]/following-sibling::td/a[contains(., 'Lançar')]"%av_desc)
        lancar_notas.click()

        for student_grade in student_grades:
            student = student_grade[0]
            grade = student_grade[1]
            try:
                # import pdb; pdb.set_trace()
                input_nota_aluno = browser.find_element("xpath", "//a[text()='%s']/../..//input[contains(@name, 'NOTA')]" % student)
                input_nota_aluno.send_keys(Keys.BACKSPACE*10)
                input_nota_aluno.send_keys(grade.replace(".", ","))
            except:                    
                erros.append(student_grade)
            # import pdb;pdb.set_trace()

        browser.find_element("xpath", "//input[@value='Salvar']").click()
    except:
        print("Algo deu errado no lançamento")
    browser.close()
    return erros

if __name__=="__main__":

    file_name = sys.argv[1]
    login = sys.argv[2]
    password = sys.argv[3]
    milestone = sys.argv[4]
    # import pdb;pdb.set_trace()
    # print("Informe o Login no academico: ")
    # login = input()
    # print("Informe a senha no academico: ")
    # password = input()
    # print("Informe a etapa: \n1BIM, \n2BIM, \n3BIM \n4BIM \nA1 (para superior)\n: ")
    # milestone = input()
    # Set the path to the academico subfolder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    academico_path = os.path.join(script_dir, "arquivos_de_atividades")

    # Use a list comprehension to get all CSV files in the subfolder
    csv_to_academico(file_name, milestone, login, password)
    # csv_files = [csv_to_academico(os.path.join(academico_path, f), milestone, login, password) for f in os.listdir(academico_path) if f.endswith('.csv')]

    