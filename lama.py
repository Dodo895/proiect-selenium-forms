
import ollama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

print("Robotul se gândește la o întrebare nouă...")

raspuns_ai = ollama.chat(model='llama3', messages=[
    {
        'role': 'user', 
        'content': 'Scrie o singură întrebare interesantă pentru un quiz de programare. Nu scrie nimic altceva, doar întrebarea.'
    }
])

intrebare_generata = raspuns_ai['message']['content']
print(f"Întrebare găsită: {intrebare_generata}")

driver = webdriver.Chrome()

element_activ = driver.switch_to.active_element

element_activ.send_keys(Keys.CONTROL, 'a')
element_activ.send_keys(Keys.BACKSPACE)

element_activ.send_keys(intrebare_generata)

time.sleep(2)