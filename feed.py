import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrage_feed_youtube(subiect_cautat, numar_videouri=10):
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("detach", True) 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    subiect_formatat = subiect_cautat.replace(" ", "+")
    driver.get(f"https://www.youtube.com/results?search_query={subiect_formatat}")

    time.sleep(4) 

    try:
        div_accept = driver.find_element(
            By.XPATH, "//button[contains(., 'Accept all') or contains(., 'Acceptați tot')]//div[@class='ytSpecTouchFeedbackShapeFill']"
        )
        driver.execute_script("arguments[0].click();", div_accept)
        time.sleep(2) 
    except:
        pass

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='video-title']")))
        videoclipuri = driver.find_elements(By.XPATH, "//a[@id='video-title']")
        
        nume_fisier = "feed_youtube.txt"
        
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            fisier.write(f"REZULTATE YOUTUBE PENTRU: {subiect_cautat.upper()}\n")
            
            postari_salvate = 0
            for video in videoclipuri:
                titlu = video.get_attribute("title")
                link = video.get_attribute("href")
                
                if titlu and link:
                    postari_salvate += 1
                    fisier.write(f"{postari_salvate}. {titlu}\n")
                    fisier.write(f"   Link: {link}\n")
                    fisier.write("-" * 40 + "\n")
                    
                if postari_salvate >= numar_videouri:
                    break
                    
        print(f"GATA! Fisierul '{nume_fisier}' a fost salvat cu succes.")
        
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    extrage_feed_youtube("tocanita de ceapa", 5)