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
from PIL import Image, ImageTk

gif_animation_id = None

def saa_temp(event = None):
    global gif_animation_id
    linn = entry.get().lower().strip().replace("-", "").replace("ü", "u").replace("ö", "o").replace("õ", "o").replace("ä", "a")
    label_result.config(text = "Laen...", font = font1)
    gif_label.config(image='')
    gif_label.image = None

    if gif_animation_id is not None:
        root.after_cancel(gif_animation_id)
        gif_animation_id = None

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
            play_gif("icon_sun.gif", gif_label)

        except Exception as e:
            label_result.config(text="Kontrolli nime", font = font1)
        finally:
            driver.quit()

    threading.Thread(target=run).start() 

def play_gif(path, label):
    frames = []
    gif = Image.open(path)

    try:
        while True:
            frame = ImageTk.PhotoImage(gif.copy())
            frames.append(frame)
            gif.seek(len(frames))
    except:
        pass

    def update(index):
        frame = frames[index]
        label.configure(image=frame)
        label.image = frame
        
        global gif_animation_id
        gif_animation_id = root.after(500, update, (index + 1) % len(frames))

    update(0)


root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)
root.title("Ilm")
root.geometry("400x200")
root.configure(bg="beige")
root.bind('<Return>', saa_temp)


font1 = TkFont.Font(family="Arial",size=12,weight="bold")
font2 = TkFont.Font(family="Arial",size=12)

label = tk.Label(root, text="Sisesta Eesti linn: ", font = font1)
label.pack(pady=(25, 5))
label.configure(bg = "beige")

entry = tk.Entry(root, font= font2)
entry.pack(pady=5)


button = tk.Button(root, text="Otsi", command=saa_temp, font = font1)
button.pack(pady=5)
button.configure(bg = "burlywood3")

result_frame = tk.Frame(root, bg="beige")
result_frame.pack(pady=10)

label_result = tk.Label(result_frame, text="", font=font1, bg="beige")
label_result.pack(side="left", padx=(0, 10))

gif_label = tk.Label(result_frame, bg="beige")
gif_label.pack(side="left")

root.mainloop()
