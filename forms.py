import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

def automatizare_forms():
    print("Porneste")
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_experimental_option("detach",True) 

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://forms.office.com/")
    print("Ai 120 de secunde sa te loghezi")
    time.sleep(120)

    toate_taburile=driver.window_handles 
    driver.switch_to.window(toate_taburile[0])

    print("Inapoi pe primul Tab.Ai 20 de secunde sa te loghezi")
    driver.get("https://forms.office.com/")
    time.sleep(20)

    return driver 

def creare_formular(driver,titlu_formular="Chestionar"):
    print(f"Incepem crearea formularului: {titlu_formular}")
    wait=WebDriverWait(driver,15)

    try:
        print("Caut butonul Chestionar")
        buton_xpath=(
            "//button[contains(@aria-label, 'Formular') or contains(@aria-label, 'Chestionar') or contains(@aria-label, 'New form')] | "
            "//div[@role='button' and (contains(., 'Formular') or contains(., 'Chestionar') or contains(., 'New'))] | "
            "//button[contains(., 'Formular') or contains(., 'Chestionar')]"
            )
        buton_nou=wait.until(EC.element_to_be_clickable((By.XPATH,buton_xpath)))
        try:
            buton_nou.click()
        except:
            driver.execute_script("arguments[0].click();",buton_nou)
        print(f"Acum sunt pe linkul:{driver.current_url}")

        print("1. Intru in campul de titlu (click pe text)")
        span_titlu=wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Formular fara titlu') or contains(text(), 'Untitled form')]")
        ))
        try:
            span_titlu.click()
        except:
            driver.execute_script("arguments[0].click();",span_titlu)
        time.sleep(2)
        
        print("2.Pun titlul")
        titlu_xpath= "//div[@role='textbox' and (contains(@aria-label, 'Titlu') or contains (@aria-label, 'title'))]"
        titlu_element=wait.until(EC.presence_of_element_located((By.XPATH,titlu_xpath)))
        try:
            titlu_element.click()
        except:
            driver.execute_script("arguments[0].click();",titlu_element)
        time.sleep(1)

        titlu_element.send_keys(Keys.CONTROL,'a')
        titlu_element.send_keys(Keys.BACKSPACE)
        titlu_element.send_keys(titlu_formular)
        time.sleep(2)

        for i in range(1,4):
            print(f"Adaugam intreabrea cu numarul {i}")
            print("Apas pe butonul Adaugare")
            btn_adaugare=wait.until(EC.presence_of_element_located(
                (By.XPATH,"//span[text()='Pornire rapidă cu' or text()='Adăugați o întrebare nouă']")
            ))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_adaugare)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_adaugare)
            time.sleep(2)

            print("4. Apas pe Alegere...")
            btn_alegere = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Alegere'] | //span[text()='Alegere']")
            ))
            driver.execute_script("arguments[0].click();", btn_alegere)
            time.sleep(2)

            print("5. Apas pe titlul intrebarii si scriu...")
            input_intrebare = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Întrebare']")
            ))
            try:
                input_intrebare.click()
            except:
                driver.execute_script("arguments[0].click();", input_intrebare)
            time.sleep(1)

            element_activ = driver.switch_to.active_element
            element_activ.send_keys(Keys.CONTROL, 'a')
            element_activ.send_keys(Keys.BACKSPACE)
            element_activ.send_keys(f"Intrebare {i}: Selectati optiunea dorita")
            time.sleep(1)

            print("6. Pun Optiunea 1...")
            input_opt1 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Opțiune 1']")
            ))
            try:
                input_opt1.click()
            except:
                driver.execute_script("arguments[0].click();", input_opt1)
            time.sleep(1)
            
            element_activ = driver.switch_to.active_element
            element_activ.send_keys(Keys.CONTROL, 'a')
            element_activ.send_keys(Keys.BACKSPACE)
            element_activ.send_keys("Da")
            time.sleep(1)

          
            print("7. Pun Optiunea 2...")
            input_opt2 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Opțiune 2']")
            ))
            try:
                input_opt2.click()
            except:
                driver.execute_script("arguments[0].click();", input_opt2)
            time.sleep(1)
            
            element_activ = driver.switch_to.active_element
            element_activ.send_keys(Keys.CONTROL, 'a')
            element_activ.send_keys(Keys.BACKSPACE)
            element_activ.send_keys("Nu")

            print(f"Intrebarea {i} e gata!")
            time.sleep(2)

    except Exception as e:
        print(f"Eroare intampinata: {e}")

driver_activ = automatizare_forms()
creare_formular(driver_activ, "Feedback 2024")