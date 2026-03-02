import tkinter
import requests
from tkinter import scrolledtext
from threading import Thread

def check():
    for i in urls:
        response = requests.get(i)
        code = response.status_code
        status = {
            200: "доступен",
            202: "доступен, но обработка ещё не завершена"
        }.get(code, "не доступен")
        if 400 <= code < 600:
            status = "ошибка сервера"
        text.insert(tkinter.END, f"{i} – {status} – {code}\n")

urls = [
    'https://github.com/',
    'https://www.binance.com/en',
    'https://tomtit.tomsk.ru/',
    'https://jsonplaceholder.typicode.com/',
    'https://moodle.tomtit-tomsk.ru/'
]

root = tkinter.Tk()
root.title("URL Checker")

label = tkinter.Label(root, text = "Проверка сайтов")
label.pack()
text = scrolledtext.ScrolledText(root)
text.pack()

Thread(target = check).start()

root.mainloop()