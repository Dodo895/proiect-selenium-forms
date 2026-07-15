from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3
import datetime

def curata_pretul(pret_text):
    if pret_text == "Pret indisponibil/Epuizat":
        return 0.0
    pret = pret_text.replace("Lei","").replace("lei","").strip()
    pret = pret.replace(".","")
    pret = pret.replace(",",".").replace(" ",".")
    return float(pret)


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

print("Pornim robotul...")
browser = webdriver.Chrome()
lista_produse = [
    "https://www.emag.ro/biblia-sau-sfanta-scriptura-format-053-alba-patriarhia-romana-cns322/pd/D1GGX6BBM/",
    "https://www.emag.ro/banda-de-alergat-electrica-orion-sprint-c1-bluetooth-fitshow-kinomap-zwift-viteza-maxima-12-km-h-greutate-maxima-suportata-100kg-pliabila-12-programe-presetate-sprintc1/pd/D6SWG8BBM/",
    "https://www.emag.ro/telefon-mobil-samsung-galaxy-a16-dual-sim-128gb-4gb-ram-4g-light-green-sm-a165flgbeue/pd/DJJ1YZYBM/"
]


while True:
    print("Se da refresh la preturi")
    
   
    for i in lista_produse:
        browser.get(i)
        time.sleep(3)

        titlu = browser.find_element(By.TAG_NAME,"h1").get_attribute("textContent").strip()

        try:
            pret_brut = browser.find_element(By.CSS_SELECTOR,".product-new-price").get_attribute("textContent").strip()
        except:
            pret_brut = "Pret indisponibil/Epuizat"

        pret_curat = curata_pretul(pret_brut)
        data_acum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
        INSERT INTO istoric_preturi (nume_produs, pret, data_verificare)
        VALUES (?, ?, ?)
        """, (titlu, pret_curat, data_acum))
        conn.commit()
        
        print(f"Salvat in DB: {titlu} | {pret_curat} lei")
    
   
    print("Asteptam 60 de secunde...")
    time.sleep(60)

browser.quit()
conn.close()
print("S-a extras cu succes")