import undetected_chromedriver.v2 as uc
from time import sleep
import time
username = 'dpex.guarus@gmail.com'
password ='dpex@2018'

driver = uc.Chrome(version_main=106)

driver.delete_all_cookies()

driver.get('https://accounts.google.com/ServiceLogin')
sleep(2)

driver.find_element("xpath",'//input[@type="email"]').send_keys(username)
driver.find_element("xpath", '//*[@id="identifierNext"]').click()
sleep(2)
driver.find_element("xpath", '//input[@type="password"]').send_keys(password)
driver.find_element("xpath", '//*[@id="passwordNext"]').click()
sleep(2)
timesum = 0
for i in range(10):
    driver.get("https://oportunidadesiff.glideapp.io")
    btn = None
    while (True):
        try:
            btn = driver.find_element("id", "sign-in-with-google-button")
            break
        except:
            print("Aguardando botão de login com google")
    btn.click()
    if i > 0:
        w = driver.window_handles[1]
        driver.switch_to.window(w)
        driver.find_element("xpath", '//div[@data-identifier="dpex.guarus@gmail.com"]').click()
        sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        





    start = time.time()
    while(True):
        try:
            driver.find_element("id", "reload-area")

        except:
            driver.get("https://oportunidadesiff.glideapp.io")
        break
    while(True):
        try:
            # import pdb; pdb.set_trace()
            driver.find_element("xpath", '//div[@role="navigation"]')
            break
        except:
            print("aguardando tela inicial aparecer")
    end = time.time()
    
    timesum += end - start
    # import pdb;pdb.set_trace()
    while(True):
        try:
            driver.find_element("xpath", '//button[@data-test="nav-button-menu"]').click()
            sleep(1)
            driver.find_element("xpath", '//div[contains(text(), "Out")]/..').click()
            break
        except:
            print("Cannot open nav")

    

print(timesum/10)

# driver.find_element_by_id("sign-in-with-google-button").click()
# w = driver.window_handles[1]
# driver.switch_to.window(w)
# bw.find_element_by_id("identifierId").send_keys("thiagorinu@gmail.com")
# nextButton = bw.find_elements_by_xpath('//*[@id ="identifierNext"]')
# nextButton[0].click()