from ast import Try
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import uuid

bw = webdriver.Firefox(executable_path="./geckodriver")
bw.get("https://suap.iff.edu.br")
bw.maximize_window()
usr = bw.find_element("id", "id_username")
pwd = bw.find_element("id", "id_password")
submit = bw.find_element("xpath", "//input[@value='Acessar']")
usr.send_keys("2163204")
pwd.send_keys("!C}Xx+p61[0M$vIA.xM#aI")
submit.click()
bw.get("https://suap.iff.edu.br/djtools/breadcrumbs_reset/pesquisaeextens%C3%A3o_projetos_monitoramento/sisep/projetos_em_execucao/")
# year = bw.find_element("id", "id_ano")
# year_sel = Select(year)
# year_sel.select_by_visible_text("2022")
sb = bw.find_element("name", "buscaprojeto_form")
sb.click()


elems = bw.find_elements(By.PARTIAL_LINK_TEXT, "Visualizar")

table = [["Projeto ID", "Título do Projeto", "Tipo do projeto", "Início da Execução", "Término da Execução", "Área do Conhecimento", "Área Temática", "Resumo"]]

servidores = []
participacoes = [["Projeto ID", "Participante"]]
table_line = []
cont = 0
while True:
    cont += 1
    try:
        view_link_index = 0
       
        while view_link_index < len(elems):
            current_url = bw.current_url
            view_link = bw.find_elements(By.PARTIAL_LINK_TEXT, "Visualizar")[view_link_index]
            table_line = [view_link.get_attribute("href")]
            view_link_index += 1
            view_link.click()
            
            prev = ""
            time.sleep(1)
            tds = [td.text for td in bw.find_elements(By.TAG_NAME, "td")]
            table_line = table_line + [tds[i+1] for i, t in enumerate(tds) if t in ["Título do Projeto", "Tipo do projeto", "Início da Execução", "Término da Execução", "Área do Conhecimento", "Área Temática", "Resumo"]]
            
            print(table_line)
            # import pdb;pdb.set_trace()
            if "2021" in table_line[4] or "2022" in table_line[4]:
                bw.get(current_url)
                continue
            table.append(table_line)
            bw.find_element("xpath", "//a[@data-tab='equipe']").click()
            time.sleep(1)
            tds = [t.text for t in bw.find_elements(By.TAG_NAME, "td")]
            indexes = [i+1 for i, t in enumerate(tds) if 'Inativo' == t]
            
            inactive_names = [tds[i].split("Nome:\n")[-1].split(" (")[0] for i in indexes]
            bw.back()
            servidores_links = [l.get_attribute("href") for l in bw.find_elements("xpath", "//dd/a[contains(@href,'/rh/')]")]
            for l in servidores_links:
                bw.get(l)
                time.sleep(1)
                dts = [dt.text for dt in bw.find_elements(By.TAG_NAME, "dt")]
                dds = [dd.text for dd in bw.find_elements(By.TAG_NAME, "dd")]
                server_data = [dds[i] for i, t in enumerate(dts) if t in ["E-mail Institucional", "Nome Usual"]]
                server_data.reverse()
                servidores.append(server_data)
                # import pdb;pdb.set_trace()
                participacoes.append([table_line[0], server_data[0]])
            for l in servidores_links:
                bw.back()

            alunos_links = [l.get_attribute("href") for l in bw.find_elements("xpath", "//dd/a[contains(@href,'/aluno/')]")]
            for l in alunos_links:
                bw.get(l)
                time.sleep(1)
                dts = [dt.text for dt in bw.find_elements(By.TAG_NAME, "dt")]
                dds = [dd.text for dd in bw.find_elements(By.TAG_NAME, "dd")]

                student_data = [dds[i] for i, t in enumerate(dts) if t in ["Nome", "Matrícula", "Curso"]][:3]
                # if "Ramon" in student_data[0]:
                # import pdb;pdb.set_trace()

                if student_data[0] in inactive_names:
                    continue
                # import pdb;pdb.set_trace()
                time.sleep(1)
                # bw.find_element("xpath", "//h3[@title='Mostrar informações']").click()
                email = ""
                # time.sleep(1)
                try:
                    email = bw.find_element("xpath", "//p[contains(., 'gsuite')]").text
                except:
                    try:
                        email = bw.find_element("xpath", "//p[contains(., '@')]").text
                    except:
                        bw.get(current_url)
                        continue


                    
                student_data = [email] + student_data
                servidores.append(student_data)
                participacoes.append([table_line[0], student_data[0]])
                
            bw.get(current_url)
                
            
            # import pdb;pdb.set_trace()
        bw.find_element(By.PARTIAL_LINK_TEXT, "próximo").click()
        
    except Exception as e:
        print(e)
        import pdb;pdb.set_trace()
        break
    # if cont == 5:
        # break
# import pdb;pdb.set_trace()

bw.close()
        

with open('projects.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    for row in table:
        wr.writerow(row)

with open('particip.csv', 'w', newline='') as csvfile:
   wr = csv.writer(csvfile)
   for row in participacoes:
       wr.writerow(row)

with open('users.csv', 'w', newline='') as csvfile:
   wr = csv.writer(csvfile)
   for row in servidores:
       wr.writerow(row)
