import psutil
import time
import tkinter
from tkinter import scrolledtext
from threading import Thread

def check():
    while True:
        cpu = psutil.cpu_percent(interval = 1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        text.delete(1.0, tkinter.END)

        text.insert(tkinter.END,f"Загрузка CPU за 1 сек: {cpu}% - Использование RAM: {ram}% - Использование диска: {disk}%")

        time.sleep(1)

root = tkinter.Tk()
root.title("Sys check")

label = tkinter.Label(root, text = "Системный мониторинг")
label.pack()
text = scrolledtext.ScrolledText(root, width = 85)
text.pack()

Thread(target = check).start()

root.mainloop()