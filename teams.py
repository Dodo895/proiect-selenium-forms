from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def trimite_mesaje_teams():
    lista_utilizatori=[
        "andrei-valentin.lazarescu@stud.mta.ro",
        "daniel-iosif.ogrin@stud.mta.ro",
        "mircea-florin.corbu@stud.mta.ro"
        ]
    mesaj_de_trimis="Daca vezi asta deja e un indian in pc-ul tau fugi."
    print("Pornim teams")
    optiuni = Options()
    optiuni.add_argument('--no-sandbox')               
    optiuni.add_argument('--disable-dev-shm-usage')   
    
    browser = webdriver.Chrome(options=optiuni)
    browser.get("https://teams.microsoft.com/")

    print("Ai 150 secunde sa completezi")
    time.sleep(150)

    wait=WebDriverWait(browser,15)

    for utilizator in lista_utilizatori:

        try:
            bara_cautare=wait.until(EC.element_to_be_clickable((By.XPATH,'//input[contains(@placeholder, "Search") or contains(@placeholder, "Căutați") or @role="combobox"]')))
            bara_cautare.send_keys(Keys.CONTROL + "a")
            time.sleep(0.5)
            bara_cautare.send_keys(Keys.DELETE)
            time.sleep(1)
            bara_cautare.send_keys(utilizator)
            print("Se cauta utilizatorul")
            time.sleep(4)
            bara_cautare.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            bara_cautare.send_keys(Keys.ENTER)
            print("Am selectat chatul")
            time.sleep(6)
            casuta_mesaj = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@contenteditable="true"]')))
            casuta_mesaj.click()
            time.sleep(1)
            casuta_mesaj.send_keys(mesaj_de_trimis)
            time.sleep(1)
            casuta_mesaj.send_keys(Keys.ENTER)
            print(f"=> Mesajul catre {utilizator} a fost trimis")
        except:
            print(f"Eroare")
        time.sleep(4)


    print("Toate mesajele au fost transmise")
    browser.quit()

trimite_mesaje_teams()



