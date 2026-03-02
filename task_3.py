import requests
import json
import tkinter
from tkinter import scrolledtext, messagebox

url = "https://www.cbr-xml-daily.ru/daily_json.js"
data = requests.get(url, timeout = 5).json()
list_groups = {}

def viewing_all_currencies():
    text.delete(1.0, tkinter.END)

    for code, info in data['Valute'].items():
        text.insert(tkinter.END, f"{code}: {info['Name']} - {info['Value']} руб.\n")

def viewing_specific_currency():
    text.delete(1.0, tkinter.END)

    code = entry.get().upper()
    if code in data['Valute']:
        i = data['Valute'][code]
        text.insert(tkinter.END, f"{code}: {i['Name']}\nНоминал: {i['Nominal']}\nКурс: {i['Value']} руб.")
    else:
        text.insert(tkinter.END, f"Ошибка: валюта с кодом '{code}' не найдена!")

def update_groups_listbox():
    group_list.delete(0, tkinter.END)

    for group_name in list_groups.keys():
        group_list.insert(tkinter.END, group_name)

def create_group_currency():
    name = group_entry.get().lower()

    if not name:
        messagebox.showerror("Ошибка", "Введите название группы!")
        return
    if name in list_groups:
        messagebox.showerror("Ошибка", f"Группа '{name}' уже есть!")
    else:
        list_groups[name] = []
        messagebox.showinfo("Успех", f"Группа '{name}' создана")
        group_entry.delete(0, tkinter.END)
        update_groups_listbox()

def view_selected_group():
    if not group_list.curselection():
        messagebox.showerror("Ошибка", "Сначала выберите группу в списке!")
        return
    text.delete(1.0, tkinter.END)
    selected_index = group_list.curselection()[0]
    group_name = group_list.get(selected_index)
    text.insert(tkinter.END, f"Содержимое группы '{group_name}':\n")
    if list_groups[group_name]:
        for currency in list_groups[group_name]:
            text.insert(tkinter.END, f"{currency['code']}: {currency['name']} - {currency['value']} руб.\n")
    else:
        text.insert(tkinter.END, "(группа пуста)")

def add_to_group():
    if not group_list.curselection():
        messagebox.showerror("Ошибка", "Сначала выберите группу в списке!")
        return
    selected_index = group_list.curselection()[0]
    group_name = group_list.get(selected_index)
    currency_code = entry.get().upper()
    if not currency_code:
        messagebox.showerror("Ошибка", "Введите код валюты в поле!")
        return
    if currency_code not in data['Valute']:
        messagebox.showerror("Ошибка", f"Валюта '{currency_code}' не найдена!")
        return
    for currency in list_groups[group_name]:
        if currency['code'] == currency_code:
            messagebox.showerror("Ошибка", f"Валюта '{currency_code}' уже есть в группе!")
            return
    currency_info = data['Valute'][currency_code]
    new_currency = {
        'code': currency_code,
        'name': currency_info['Name'],
        'nominal': currency_info['Nominal'],
        'value': currency_info['Value']
    }
    list_groups[group_name].append(new_currency)
    messagebox.showinfo("Успех", f"Валюта '{currency_code}' добавлена в группу!")
    entry.delete(0, tkinter.END)
    view_selected_group()

def save_groups_to_file():
    if not list_groups:
        messagebox.showerror("Ошибка", "Нет групп для сохранения!")
        return
    with open("resourse/save.json", "w") as file:
        json.dump(list_groups, file)
    messagebox.showinfo("Успех", "Группы сохранены в файл save.json")

def load_groups_from_file():
    global list_groups

    try:
        with open("resourse/save.json", "r") as file:
            list_groups = json.load(file)
        update_groups_listbox()
        messagebox.showinfo("Успех", "Группы загружены из файла save.json")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл save.json не найден!")

root = tkinter.Tk()
root.title("Курсы валют")
root.geometry("800x800")

main_frame = tkinter.Frame(root)
main_frame.pack()

tkinter.Label(main_frame, text = "Код валюты:").pack(anchor = 'w')
entry = tkinter.Entry(main_frame, width = 20)
entry.pack(anchor = 'w')

button_frame = tkinter.Frame(main_frame)
button_frame.pack(anchor = 'w')
tkinter.Button(button_frame, text = "Найти", command = viewing_specific_currency).pack(side = 'left')
tkinter.Button(button_frame, text = "Все валюты", command = viewing_all_currencies).pack(side = 'left')

tkinter.Label(main_frame, text = "Новая группа:").pack(anchor = 'w')
group_entry = tkinter.Entry(main_frame)
group_entry.pack(anchor = 'w')
tkinter.Button(main_frame, text = "Создать", command = create_group_currency).pack(anchor = 'w')

tkinter.Label(main_frame, text = "Группы:").pack(anchor = 'w')
group_list = tkinter.Listbox(main_frame)
group_list.pack(anchor = 'w')

group_buttons_frame = tkinter.Frame(main_frame)
group_buttons_frame.pack(anchor = 'w')
tkinter.Button(group_buttons_frame, text = "Показать группу", command = view_selected_group).pack(side = 'left')
tkinter.Button(group_buttons_frame, text = "Добавить в группу", command = add_to_group).pack(side = 'left')

save_buttons_frame = tkinter.Frame(main_frame)
save_buttons_frame.pack(anchor = 'w')
tkinter.Button(save_buttons_frame, text = "Сохранить в save.json", command = save_groups_to_file).pack(side = 'left')
tkinter.Button(save_buttons_frame, text = "Загрузить из save.json", command = load_groups_from_file).pack(side = 'left')

text = scrolledtext.ScrolledText(main_frame)
text.pack(anchor = 'w')

viewing_all_currencies()
root.mainloop()