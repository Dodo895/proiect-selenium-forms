import streamlit as st
import time
import sqlite3
import datetime
import ollama
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def extrage_youtube(subiect_cautat, numar_videouri):
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    subiect_formatat = subiect_cautat.replace(" ", "+")
    driver.get(f"https://www.youtube.com/results?search_query={subiect_formatat}")
    time.sleep(4) 
    try:
        div_accept = driver.find_element(By.XPATH, "//button[contains(., 'Accept all') or contains(., 'Acceptați tot')]//div[@class='ytSpecTouchFeedbackShapeFill']")
        driver.execute_script("arguments[0].click();", div_accept)
        time.sleep(2) 
    except:
        pass
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='video-title']")))
        videoclipuri = driver.find_elements(By.XPATH, "//a[@id='video-title']")
        nume_fisier = "feed_youtube.txt"
        postari_salvate = 0
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            fisier.write(f"REZULTATE YOUTUBE PENTRU: {subiect_cautat.upper()}\n")
            for video in videoclipuri:
                titlu = video.get_attribute("title")
                link = video.get_attribute("href")
                if titlu and link:
                    postari_salvate += 1
                    fisier.write(f"{postari_salvate}. {titlu}\n   Link: {link}\n" + "-" * 40 + "\n")
                if postari_salvate >= int(numar_videouri):
                    break
        return True, nume_fisier
    except Exception as e:
        return False, str(e)


def ruleaza_forms(titlu_formular_baza, numar_formulare):
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://forms.office.com/")
        time.sleep(120)

        toate_taburile = driver.window_handles 
        driver.switch_to.window(toate_taburile[0])
        driver.get("https://forms.office.com/")
        time.sleep(45)

        wait = WebDriverWait(driver, 15)

        for numar in range(1, int(numar_formulare) + 1):
            titlu_curent = f"{titlu_formular_baza} - Partea {numar}"
            
            buton_xpath = (
                "//button[contains(@aria-label, 'Formular') or contains(@aria-label, 'Chestionar') or contains(@aria-label, 'New form')] | "
                "//div[@role='button' and (contains(., 'Formular') or contains(., 'Chestionar') or contains(., 'New'))] | "
                "//button[contains(., 'Formular') or contains(., 'Chestionar')]"
            )
            buton_nou = wait.until(EC.element_to_be_clickable((By.XPATH, buton_xpath)))
            
            try:
                buton_nou.click()
            except:
                driver.execute_script("arguments[0].click();", buton_nou)
                
            time.sleep(6) 

            driver.switch_to.window(driver.window_handles[-1])

            span_titlu = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Formular fără titlu') or contains(text(), 'Untitled form') or contains(text(), 'fara titlu')]")
            ))
            try:
                span_titlu.click()
            except:
                driver.execute_script("arguments[0].click();", span_titlu)
            time.sleep(2)

            titlu_xpath = "//div[@role='textbox' and (contains(@aria-label, 'Titlu') or contains(@aria-label, 'title'))]"
            titlu_element = wait.until(EC.presence_of_element_located((By.XPATH, titlu_xpath)))
            
            try:
                titlu_element.click()
            except:
                driver.execute_script("arguments[0].click();", titlu_element)
            time.sleep(1) 
            
            titlu_element.send_keys(Keys.CONTROL, 'a')
            titlu_element.send_keys(Keys.BACKSPACE)
            titlu_element.send_keys(titlu_curent)
            time.sleep(2)

            for i in range(1, 4):
                btn_adaugare = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//span[text()='Pornire rapidă cu' or text()='Adăugați o întrebare nouă']")
                ))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_adaugare)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", btn_adaugare)
                time.sleep(2)

                btn_alegere = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Alegere'] | //span[text()='Alegere']")
                ))
                driver.execute_script("arguments[0].click();", btn_alegere)
                time.sleep(2)

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
                time.sleep(2)
            
            if len(driver.window_handles) > 1:
                driver.close()
            
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://forms.office.com/")
            time.sleep(8)
            
        return True, f"Robotul a creat cu succes {numar_formulare} formulare!"
    except Exception as e:
        return False, str(e)


def trimite_teams(mesaj):
    lista_utilizatori = [
        "andrei-valentin.lazarescu@stud.mta.ro",
        "daniel-iosif.ogrin@stud.mta.ro",
        "mircea-florin.corbu@stud.mta.ro"
    ]
    optiuni = Options()
    optiuni.add_experimental_option("detach", True)   
    
    browser = webdriver.Chrome(options=optiuni)
    browser.get("https://teams.microsoft.com/")
    time.sleep(60) 

    wait = WebDriverWait(browser, 15)
    
    succese = 0
    for utilizator in lista_utilizatori:
        try:
          
            bara_cautare = wait.until(EC.element_to_be_clickable((By.XPATH,'//input[contains(@placeholder, "Search") or contains(@placeholder, "Căutați") or @role="combobox"]')))
            bara_cautare.click() 
            time.sleep(3)
            bara_cautare.send_keys(Keys.CONTROL + "a")
            time.sleep(0.5)
            bara_cautare.send_keys(Keys.BACKSPACE) 
            time.sleep(3)
            
           
            bara_cautare.send_keys(utilizator)
            time.sleep(4)
            bara_cautare.send_keys(Keys.ARROW_DOWN)
            time.sleep(5)
            bara_cautare.send_keys(Keys.ENTER)
            time.sleep(6) 
            casute_mesaj = browser.find_elements(By.XPATH, '//*[@contenteditable="true"]')
            
            for casuta in casute_mesaj:
                if casuta.is_displayed(): 
                    try:
                        casuta.click()
                        time.sleep(1)
                        casuta.send_keys(mesaj)
                        time.sleep(1)
                        casuta.send_keys(Keys.ENTER)
                        succese += 1
                        break 
                    except:
                        pass
        except Exception as e:

            pass
        
        time.sleep(4) 
        
    return True, f"S-au trimis mesaje către {succese}/{len(lista_utilizatori)} persoane."


def curata_pretul(pret_text):
    if pret_text == "Pret indisponibil/Epuizat":
        return 0.0
    pret = pret_text.replace("Lei","").replace("lei","").strip()
    pret = pret.replace(".","")
    pret = pret.replace(",",".").replace(" ",".")
    return float(pret)

def extrage_emag():
    conn = sqlite3.connect("emag_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS istoric_preturi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume_produs TEXT,
        pret REAL,
        data_verificare TEXT
    )
    """)
    conn.commit()

    options = Options()
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)
    
    lista_produse = [
        "https://www.emag.ro/biblia-sau-sfanta-scriptura-format-053-alba-patriarhia-romana-cns322/pd/D1GGX6BBM/",
        "https://www.emag.ro/banda-de-alergat-electrica-orion-sprint-c1-bluetooth-fitshow-kinomap-zwift-viteza-maxima-12-km-h-greutate-maxima-suportata-100kg-pliabila-12-programe-presetate-sprintc1/pd/D6SWG8BBM/",
        "https://www.emag.ro/telefon-mobil-samsung-galaxy-a16-dual-sim-128gb-4gb-ram-4g-light-green-sm-a165flgbeue/pd/DJJ1YZYBM/"
    ]

    for i in lista_produse:
        browser.get(i)
        time.sleep(3)
        try:
            titlu = browser.find_element(By.TAG_NAME,"h1").get_attribute("textContent").strip()
        except:
            titlu = "Produs Necunoscut"

        try:
            pret_brut = browser.find_element(By.CSS_SELECTOR,".product-new-price").get_attribute("textContent").strip()
        except:
            pret_brut = "Pret indisponibil/Epuizat"

        pret_curat = curata_pretul(pret_brut)
        data_acum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("INSERT INTO istoric_preturi (nume_produs, pret, data_verificare) VALUES (?, ?, ?)", 
                       (titlu, pret_curat, data_acum))
        conn.commit()
    
    browser.quit()
    conn.close()
    return True


# INTERFAȚA GRAFICĂ STREAMLIT

st.set_page_config(page_title="Centru de Comandă Automatizări", layout="wide")

st.sidebar.title("🤖 Meniu Roboți")
alegere = st.sidebar.radio("Alege ce automatizare vrei să folosești:", 
                           ["Extractor YouTube", "Formulare Automate", "Chat LLM (Fără API)", "Spammer Teams", "Tracker eMAG"])

if alegere == "Extractor YouTube":
    st.title("🎥 Extractor Date YouTube")
    subiect = st.text_input("Subiect de căutare:", placeholder="ex: retete de prajituri")
    numar = st.number_input("Câte videoclipuri extragem?", min_value=1, max_value=50, value=5)
    
    if st.button("Pornește Robotul YouTube"):
        with st.spinner("Se extrag datele..."):
            succes, msg = extrage_youtube(subiect, numar)
            if succes:
                st.success(f"Fișier salvat: {msg}")
                with open(msg, "r", encoding="utf-8") as file:
                    st.download_button(label="Descarcă Fișierul", data=file, file_name=msg, mime="text/plain")

elif alegere == "Formulare Automate":
    st.title("📝 Creator Automate Microsoft Forms (Multiplicare Simplă)")
    st.info("Atenție: Ai 120 de secunde inițial + încă 45 de secunde după refresh, exact cum ai cerut!")
    
    titlu = st.text_input("Titlul de bază al formularului:", value="Feedback 2026")
    numar_form = st.number_input("Câte formulare vrei să genereze robotul?", min_value=1, max_value=50, value=3)
    
    if st.button("Pornește Crearea Formularelor"):
        with st.spinner("Robotul rulează. Te rog urmărește browser-ul pentru login!"):
            succes, msg = ruleaza_forms(titlu, numar_form)
            if succes:
                st.success(msg)
            else:
                st.error(f"S-a oprit din cauza unei erori: {msg}")

elif alegere == "Chat LLM (Fără API)":
    st.title("💬 Interogare Modele LLM Locale")
    st.write("Aici poți trimite prompt-uri către diverse LLM-uri instalate pe sistemul tău, folosind motorul Ollama.")
    
   
    try:
        lista_modele_brut = ollama.list()
        modele_disponibile = [model['name'] for model in lista_modele_brut['models']]
    except:
        modele_disponibile = ["llama3"] 

    if not modele_disponibile:
        modele_disponibile = ["llama3"]
        
    model_selectat = st.selectbox("Selectează LLM-ul dorit:", modele_disponibile)
    
    prompt_utilizator = st.text_area("Introdu prompt-ul tău:", height=150, placeholder="Ce dorești să întrebi LLM-ul?")
    
    if st.button("Trimite Prompt"):
        if prompt_utilizator.strip() == "":
            st.warning("Te rog să introduci un prompt valid!")
        else:
            with st.spinner(f"Așteptăm răspunsul de la {model_selectat}..."):
                try:
                    raspuns = ollama.chat(model=model_selectat, messages=[
                        {'role': 'user', 'content': prompt_utilizator}
                    ])
                    st.markdown("### Răspuns:")
                   
                    st.write(raspuns['message']['content'])
                except Exception as e:
                    st.error(f"Eroare la generare: {str(e)}\n\nAsigură-te că modelul {model_selectat} este corect descărcat cu 'ollama pull {model_selectat}'.")

elif alegere == "Spammer Teams":
    st.title("💬 Trimitere Mesaje MS Teams")
    st.info("Atenție: Ai la dispoziție 150 de secunde pentru login după ce se deschide browser-ul!")
    mesaj_text = st.text_area("Ce mesaj vrei să trimiți colegilor?", value="Salut, testez un robot!")
    
    if st.button("Trimite Mesajele"):
        with st.spinner("Așteptăm login-ul tău și trimitem mesajele..."):
            succes, msg = trimite_teams(mesaj_text)
            if succes:
                st.success(msg)

elif alegere == "Tracker eMAG":
    st.title("🛒 Tracker Prețuri eMAG (Bază de date SQLite)")
    st.write("Apasă butonul pentru a deschide site-urile, a extrage prețurile curente și a le salva în baza de date.")
    
    if st.button("Verifică Prețurile Acum"):
        with st.spinner("Robotul deschide paginile și citește prețurile..."):
            extrage_emag()
            st.success("Prețurile au fost adăugate în baza de date!")
            
    st.subheader("Istoric Bază de Date:")
    try:
        conn = sqlite3.connect("emag_tracker.db")
        df = conn.execute("SELECT id, nume_produs, pret, data_verificare FROM istoric_preturi").fetchall()
        if df:
            st.dataframe(df, column_config={
                "0": "ID", "1": "Produs", "2": "Preț (RON)", "3": "Data și Ora"
            }, use_container_width=True)
        else:
            st.write("Baza de date este goală. Apasă butonul de mai sus!")
        conn.close()
    except Exception as e:
        st.write("Baza de date nu a fost creată încă.")