from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicialize o WebDriver do Firefox
driver = webdriver.Firefox(executable_path="./geckodriver")

# Navegue até a página que contém as guias e os links
driver.get("https://conepe.guarus.iff.edu.br")  # Substitua pelo URL real

# Lista de guias (tabs)
tabs = ["https://conepe.guarus.iff.edu.br/area-do-coordenador#area-de-concentracao-ii-ciencias-da-saude-enfermagem", "https://conepe.guarus.iff.edu.br/area-do-coordenador#area-de-concentracao-iii-ciencias-da-saude-farmacia", "https://conepe.guarus.iff.edu.br/area-do-coordenador#area-de-concentracao-vi-educacao-e-ciencias-sociais" ]
import pdb;pdb.set_trace()
# Itere por cada guia
for tab in tabs:
    driver.get("https://conepe.guarus.iff.edu.br/area-do-coordenador")
    for _ in range(2):
        driver.execute_script("window.scrollBy(0, window.innerHeight/3);")
        time.sleep(0.5)

    tab_to_click = [a for a in driver.find_elements(By.XPATH, "//a[@data-toggle='tab']") if a.get_attribute("href") == tab]
    tab_to_click[0].click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Avaliar")))
    
    # Dicionário para armazenar notas e links associados para resumos expandidos com nota > 6.0
    expandido_links = {}
    simples_links = []

    aval_links = [a.get_attribute("href") for a in driver.find_elements(By.PARTIAL_LINK_TEXT, "Avaliar")]
    for link in aval_links:
        link_href = link
        driver.get(link_href)
        
        # Verifique o tipo de resumo

        tipo_resumo = driver.find_element(By.XPATH, "//table[1]//tr[5]//td[2]").text
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        nota_element = driver.find_element(By.XPATH, "//th[text()='Nota final (média das avaliações) ']/following-sibling::th")
        nota = float(nota_element.text)
        if tipo_resumo == "Expandido" and nota >= 6.0:
            expandido_links[link_href] = nota
        
        if tipo_resumo == "Simples":
            simples_links.append([link_href, nota])

    # Pegue os 5 links mais bem avaliados
    if expandido_links:
        top_5_links = sorted(expandido_links, key=expandido_links.get, reverse=True)[:5]
        print(sorted(expandido_links, key=expandido_links.get, reverse=True))
    # import pdb;pdb.set_trace()
    for link in expandido_links:
        driver.get(link)
        
        # Se o link estiver entre os top 5, notifique como "Apresentação Oral", caso contrário, notifique como "Banner"
        formato = "oral"
        if link in top_5_links:
            message = ("É com satisfação que informamos que seu trabalho foi aprovado em formato de Apresentação Oral. "
                       "As instruções para a apresentação podem ser encontradas em https://conepe.guarus.iff.edu.br/submissoes. "
                       "Aproveite esta oportunidade para compartilhar e discutir seu trabalho com a comunidade acadêmica. "
                       "Desejamos sucesso na sua apresentação!")
        else:
            message = ("É com satisfação que informamos que seu trabalho foi aprovado em formato banner. "
                       "As instruções para a apresentação podem ser encontradas em https://conepe.guarus.iff.edu.br/submissoes. "
                       "Aproveite esta oportunidade para compartilhar e discutir seu trabalho com a comunidade acadêmica. "
                       "Desejamos sucesso na sua apresentação!")
            formato = "banner"
        
        select_formato = driver.find_element(By.ID, "avaliacao_final_formato_aprovado")
        select_formato.click()
        
        
        banner_option = driver.find_element(By.XPATH, "//option[@value='%s']"%formato)
        banner_option.click()
        
        comentarios_textarea = driver.find_element(By.ID, "avaliacao_final_comentarios")
        comentarios_textarea.send_keys(message)

        # Clique no botão "Salvar avaliação"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        salvar_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        salvar_button.click()
    
    for link in simples_links:
        driver.get(link[0])
        
        # Se o link estiver entre os top 5, notifique como "Apresentação Oral", caso contrário, notifique como "Banner"
        formato = "banner"
        if link[1] >= 6.0:
            message = ("É com satisfação que informamos que seu trabalho foi aprovado em formato de Banner. "
                       "As instruções para a apresentação podem ser encontradas em https://conepe.guarus.iff.edu.br/submissoes. "
                       "Aproveite esta oportunidade para compartilhar e discutir seu trabalho com a comunidade acadêmica. "
                       "Desejamos sucesso na sua apresentação!")
        else:
            message = ("É com pesar que informamos que seu trabalho foi rejeitado para apresentação no X CONEPE por estar abaixo da nota de corte. "
                       "Seguem as revisões para melhoria do trabalho. "
                       "De qualquer forma, agradecemos sua submissão e esperamos encontrá-lo durante a programação do evento!"
                       )
            
        
        select_formato = driver.find_element(By.ID, "avaliacao_final_formato_aprovado")
        select_formato.click()
        
        
        banner_option = driver.find_element(By.XPATH, "//option[@value='%s']"%formato)
        banner_option.click()
        
        comentarios_textarea = driver.find_element(By.ID, "avaliacao_final_comentarios")
        comentarios_textarea.send_keys(message)

        # Clique no botão "Salvar avaliação"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        salvar_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        salvar_button.click()


# Feche a janela do navegador
driver.quit()
