browser = webdriver.Firefox(executable_path="./geckodriver")
browser.get("http://www.conepe.guarus.iff.edu.br/users/sign_in")
password = browser.find_element_by_id("user_password")
login = browser.find_element_by_id('user_login')
submit = browser.find_element_by_xpath("//input[@name='commit']")
login.send_keys("126.090.107-61")
password.send_keys("thi@g0rinu")
submit.click()
final_link = "http://www.conepe.guarus.iff.edu.br/resumos_academicos/270/avaliacoes_finais/novo"
browser.get(final_link)
th_nota = browser.find_element_by_xpath("//th[contains(., 'Nota final')]/following-sibling::th")
nota = float(th_nota.get_attribute("innerHTML"))
comment = browser.find_element_by_id("avaliacao_final_comentarios")
text_aprovado = "Seu trabalho foi aprovado"
text_reprovado = "Trabalho reprovado."
if nota > 6:
    print("Trabalho Aprovado")
    sel = Select(browser.find_element_by_id("avaliacao_final_formato_aprovado"))
    sel.select_by_visible_text("Banner")
    comment.send_keys(text_aprovado)
else:
    print("Trabalho Reprovado")
    comment.send_keys(text_reprovado)

btn_salvar = browser.find_element_by_xpath("//input[@name='commit']")




