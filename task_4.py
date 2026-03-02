import requests
import tkinter
from tkinter import scrolledtext, messagebox

def get_profile():
    username = entry.get()
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    data = response.json()
    txt.delete(1.0, tkinter.END)

    if response.status_code == 200:
        txt.insert(tkinter.END,f"Имя: {data.get('name', 'Не указано')}\n")
        txt.insert(tkinter.END,f"Ссылка на профиль: {data.get('html_url', 'Не указано')}\n")
        txt.insert(tkinter.END,f"Количество репозиториев: {data.get('public_repos', 0)}\n")
        txt.insert(tkinter.END,f"Количество обсуждений: Информация недоступна через REST API\n")
        txt.insert(tkinter.END,f"Количество подписок: {data.get('following', 0)}\n")
        txt.insert(tkinter.END,f"Количество подписчиков: {data.get('followers', 0)}")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден!")

def get_repositories():
    username = entry.get()
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)

    if repos_response.status_code == 200:
        data = repos_response.json()
        txt.delete(1.0, tkinter.END)
        for i, repo in enumerate(data, 1):
            name = repo.get('name', 'Не указано')
            desc = repo.get('description', 'Нет описания')
            lang = repo.get('language', 'Не указан')
            url = repo.get('html_url', '')
            txt.insert(tkinter.END, f"{i}. {name}\n")
            txt.insert(tkinter.END, f"Описание: {desc}\n")
            txt.insert(tkinter.END, f"Язык: {lang}\n")
            txt.insert(tkinter.END, f"Ссылка: {url}\n\n")

root = tkinter.Tk()
root.title("GitHub checker")
root.geometry("600x600")

tkinter.Label(root, text = "GitHub:").pack(anchor = 'w')
entry = tkinter.Entry(root, width = 30)
entry.pack(anchor = 'w')

button_frame = tkinter.Frame(root)
button_frame.pack(anchor = 'w')

tkinter.Button(button_frame, text = "Профиль", command = get_profile).pack(side = 'left')
tkinter.Button(button_frame, text = "Репозитории", command = get_repositories).pack(side = 'left')

txt = scrolledtext.ScrolledText(root)
txt.pack(anchor = 'w')

root.mainloop()