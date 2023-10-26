import tkinter as tk 
from tkinter import scrolledtext
from random import choice

last_computer_latter = None

def check_city():
    global last_computer_latter

    city = entry.get().title()
    if not city:
        response = f"Ви не ввели місто"
    elif city in used_cities:
        response = f"Місто {city} вже було вказано!"
    elif city not in cities:
        response = f"Місто {city} відсутнє в базі даних гри"
    elif last_computer_latter and city[0] != last_computer_latter:
        response = f"Назва міста повинна починатися на {last_computer_latter}"
    else:
        used_cities.append(city)

        last_letter = get_last_latter(city)

        computer_city = get_city_by_letter(last_letter)   
        if not computer_city:
            response = f"Вітаю, Ви виграли! Я не знаю місто на літеру {last_letter}"
        else:
            used_cities.append(computer_city)
            last_computer_latter = get_last_latter(computer_city)
            response = f"Моє місто - {computer_city}"

#    response = f"Навігатор: Ви ввели {city}\n"
    game_log.config(state=tk.NORMAL)
    game_log.insert(tk.END, f"Ви: {city}\n")
    game_log.insert(tk.END, f"Навігатор: {response}\n")
    game_log.yview(tk.END)
    game_log.config(state=tk.DISABLED)
    notification.config(text=response)
    entry.delete(0, tk.END)
def get_last_latter(city):
    last_latter = city[-1].upper()
    if last_latter in ["Ь", "Й", "И"]:
        last_latter = city[-2].upper()
    return last_latter

def get_city_by_letter(letter):
    available_cities = []
    for city in cities:
        if city[0].upper() == letter and city not in used_cities:
            available_cities.append(city)
        if available_cities:
            return choice(available_cities)
    return None

def surrender():
    game_log.config(state=tk.NORMAL)
    game_log.insert(tk.END, f"Навігатор переміг!\n")
    game_log.yview(tk.END)
    game_log.config(state=tk.DISABLED)
    notification.config(text="Навігатор переміг! \n Вивчай Україну і тобі пощастить наступного разу")
    entry.delete(0, tk.END)

def load_cities_from_file(filename):
    cities = []
    with open(filename, "r", encoding="utf-8") as fd:
        for line in fd:
            cities.append(line.strip())
    return cities

cities = load_cities_from_file('cities.txt')
used_cities = []

root = tk.Tk()
root.title("Гра в міста")
root.geometry("800x400")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

label = tk.Label(left_frame, text="Введіть назву міста України")
label.pack(padx=10, pady=10)

entry = tk.Entry(left_frame, width=35)
entry.pack(padx=10, pady=10)

button_frame = tk.Frame(left_frame)
button_frame.pack(pady=10)

button = tk.Button(button_frame, text="Відправити", command=check_city)
button.pack(padx=10, side=tk.LEFT)

button_end = tk.Button(button_frame, text="Я здаюся", command=surrender)
button_end.pack(padx=10, side=tk.LEFT)

notification = tk.Label(left_frame, text="")
notification.pack(padx=10, pady=10)

game_log = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
game_log.pack(padx=10, pady=10, side=tk.RIGHT)
game_log.config(state=tk.DISABLED)

root.mainloop()
