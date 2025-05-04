from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import threading
import tkinter.font as TkFont
from ctypes import windll
from Pillow import image

def saa_temp():
    linn = entry.get().lower().replace(" ", "").replace("-", "")
    label_result.config(text = "Laen...", font = font1)
    def run():
        try:
            seaded = Options()
            seaded.add_argument("--headless")

            service = Service("D:\chromedriver-win64\chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=seaded)

            driver.get("https://ilm.ee/" + linn + "/")

            if "Lehte ei leitud" in driver.page_source or "404" in driver.title:
                raise Exception

            temperatuur_toores = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "current-temp")))
            temperatuur = temperatuur_toores.text
            label_result.config(text = f"Temperatuur: {temperatuur}", font = font1)
        except Exception as e:
            label_result.config(text="Kontrolli nime", font = font1)
        finally:
            driver.quit()

    threading.Thread(target=run).start() 


root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)
root.title("Ilm")
root.geometry("400x200")
root.configure(bg="beige")

font1 = TkFont.Font(family="Arial",size=12,weight="bold")
font2 = TkFont.Font(family="Arial",size=12)

label = tk.Label(root, text="Sisesta linn (Eestis, ilma täpitähtedeta): ", font = font1)
label.pack(pady=(25, 5))
label.configure(bg = "beige")

entry = tk.Entry(root, font= font2)
entry.pack(pady=5)


button = tk.Button(root, text="Otsi", command=saa_temp, font = font1)
button.pack(pady=5)
button.configure(bg = "burlywood3")

label_result = tk.Label(root, text="", font = font1)
label_result.pack(pady=10)
label_result.configure(bg = "beige")

root.mainloop()
