import sqlite3
import time
import threading
from tkinter import *
from tkinter import ttk

connection = sqlite3.connect('project.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
fio TEXT NOT NULL,
time TEXT NOT NULL,
kab TEXT NOT NULL
)
''')

floor1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'б/н', 'с/д', 'с/л']
floor2 = ['17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '32л', 'к/д', 'с/л']
floor3 = ['35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '48л', '48а', '49', '49л', '50', '51', '51л', '52', '53', '54', '55', 'т/с']
floor4 = ['56', '56л', '57', '57л', '58', '59', '60', '61']


def check_btn():
    labeltext2.config(text="")
    kab = entrycheckkab.get()
    cursor.execute('SELECT kab FROM Users WHERE kab = ?', (kab,))
    res = cursor.fetchone()
    if res:

        labelcheck.config(text=f"Кабинет занят.")
    else:
        labelcheck.config(text="Кабинет свободен")
    threading.Timer(4, clear_label).start()


def clear_label():
    labelcheck.config(text="")
    labeltext1.config(text="")
    labeltext2.config(text="")

def write_btn():
    labeltext2.config(text="")

    cursor.execute('SELECT MAX(id) FROM Users')
    idl = cursor.fetchone()[0]
    if idl is None:
        idl = 0
    id = (int(idl)) + 1
    fio = entryfio.get()
    kab = entrykab.get()
    time = entrytime.get()
    if kab and fio and time and id:
        cursor.execute('SELECT kab FROM Users WHERE kab = ?', (kab,))
        res = cursor.fetchone()
        if res:
            labeltext1.config(text="Кабинет занят")
        else:
            cursor.execute('INSERT INTO Users (id, fio, time, kab) VALUES (?, ?, ?, ?)',
                           (id, fio, time, kab))
            labeltext1.config(text=f"Запись: {id}")
            threading.Timer(5, clear_label).start()
    else:
        labeltext1.config(text="Неверный ввод")
    threading.Timer(4, clear_label).start()


    entryfio.delete(0, END)
    entrykab.delete(0, END)
    entrytime.delete(0, END)

def find_btn():
    labeltext2.config(text="")
    kab1 = entrykab2.get()
    fio1 = entryfio2.get()
    time1 = entrytime2.get()
    id1 = entryid.get()



    resfio = ''
    reskab = ''
    resid = ''
    restime = ''


    if id1:
        cursor.execute('SELECT fio, time, kab FROM Users WHERE id = ?', (id1,))
        result = cursor.fetchone()
        if result:
            resfio, restime, reskab = result
            resid = id1
            labeltext2.config(text="Успешно")
        else:
            labeltext2.config(text="Данные отсутствуют")
    elif fio1:
        cursor.execute('SELECT id, time, kab FROM Users WHERE fio = ?', (fio1,))
        result = cursor.fetchone()
        if result:
            resid, restime, reskab = result
            resfio = fio1
            labeltext2.config(text="Успешно")
        else:
            labeltext2.config(text="Данные отсутствуют")
    elif time1:
        cursor.execute('SELECT id, fio, kab FROM Users WHERE time = ?', (time1,))
        result = cursor.fetchone()
        if result:
            resid, resfio, reskab = result
            restime = time1
            labeltext2.config(text="Успешно")
        else:
            labeltext2.config(text="Данные отсутствуют")
    elif kab1:
        cursor.execute('SELECT fio, time, id FROM Users WHERE kab = ?', (kab1,))
        result = cursor.fetchone()
        if result:
            resfio, restime, resid = result
            reskab = kab1
            labeltext2.config(text="Успешно")
        else:
            labeltext2.config(text="Данные отсутствуют")
    else:
        labeltext2.config(text="Данные отсутствуют")




    entryfio2.delete(0, END)
    entryfio2.insert(0, resfio)

    entrykab2.delete(0, END)
    entrykab2.insert(0, reskab)

    entrytime2.delete(0, END)
    entrytime2.insert(0, restime)

    entryid.delete(0, END)
    entryid.insert(0, resid)



def delete_btn():
    kab1 = entrykab2.get()
    fio1 = entryfio2.get()
    time1 = entrytime2.get()
    id1 = entryid.get()
    if kab1 and fio1 and time1 and id1:
        cursor.execute("DELETE FROM Users WHERE id = ? AND fio = ? AND time = ? AND kab = ?", (id1, fio1, time1, kab1,))
        labeltext2.config(text="Ячейка удалена")
    else:
        labeltext2.config(text="Неверный ввод")
    threading.Timer(4, clear_label).start()

def clear_btn():
    entryfio2.delete(0, END)
    entrykab2.delete(0, END)
    entrytime2.delete(0, END)
    entryid.delete(0, END)

    entrycheckkab.delete(0, END)

    entryfio.delete(0, END)
    entrykab.delete(0, END)
    entrytime.delete(0, END)
    labeltext2.config(text="")




root = Tk()
root.title("Приложение")
root.geometry("500x300")

labeltitle1 = ttk.Label()
labeltitle1.config(text="Заполнение данных")
labeltitle1.grid(padx=6, pady=6, row=1, column=1)

labelfio = ttk.Label()
labelfio.config(text="Фио", width=20)
labelfio.grid(padx=3, pady=6, row=2, column=1)

entryfio = ttk.Entry()
entryfio.config(width=20)
entryfio.grid(padx=3, pady=6, row=3, column=1)

labelkab = ttk.Label()
labelkab.config(text="Каб")
labelkab.grid(padx=3, pady=6, row=2, column=2)

entrykab = ttk.Entry()
entrykab.config(width=3)
entrykab.grid(padx=3, pady=6, row=3, column=2)

labeltime = ttk.Label()
labeltime.config(text="Дата", width=9)
labeltime.grid(padx=3, pady=0, row=2, column=3)

entrytime = ttk.Entry()
entrytime.config(width=9)
entrytime.grid(padx=3, pady=6, row=3, column=3)

btn_write = ttk.Button(text="Заполнить", command=write_btn)
btn_write.grid(padx=3, pady=0, row=3, column=4)

btn_check = ttk.Button(text="Проверить", command=check_btn)
btn_check.grid(padx=3, pady=0, row=3, column=9)

labelcheck = ttk.Label()
labelcheck.grid(padx=0, pady=0, row=4, column=8, columnspan=2)

labeltitlecheck = ttk.Label()
labeltitlecheck.config(text="Свободные кабинеты")
labeltitlecheck.grid(padx=6, pady=6, row=2, column=8, columnspan=2)

entrycheckkab = ttk.Entry()
entrycheckkab.config(width=4)
entrycheckkab.grid(padx=3, pady=6, row=3, column=8)

labeltext1 = ttk.Label()
labeltext1.grid(padx=0, pady=0, row=2, column=4)

labeltitle2 = ttk.Label()
labeltitle2.config(text="Действия с данными")
labeltitle2.grid(padx=6, pady=6, row=6, column=1)

labelfio2 = ttk.Label()
labelfio2.config(text="Фио", width=20)
labelfio2.grid(padx=3, pady=6, row=7, column=1)

entryfio2 = ttk.Entry()
entryfio2.config(width=20)
entryfio2.grid(padx=3, pady=6, row=8, column=1)

labelkab2 = ttk.Label()
labelkab2.config(text="Каб")
labelkab2.grid(padx=3, pady=6, row=7, column=2)

entrykab2 = ttk.Entry()
entrykab2.config(width=3)
entrykab2.grid(padx=3, pady=6, row=8, column=2)

labeltime2 = ttk.Label()
labeltime2.config(text="Дата", width=9)
labeltime2.grid(padx=3, pady=0, row=7, column=3)

entrytime2 = ttk.Entry()
entrytime2.config(width=9)
entrytime2.grid(padx=3, pady=6, row=8, column=3)

btn_find = ttk.Button(text="Найти", command=find_btn)
btn_find.grid(padx=0, pady=0, row=8, column=8)

btn_clear = ttk.Button(text="Очистить", command=clear_btn)
btn_clear.grid(padx=0, pady=0, row=8, column=9)

btn_delete = ttk.Button(text="Удалить запись", command=delete_btn)
btn_delete.grid(padx=0, pady=0, row=9, column=8, columnspan=2)

labeltext2 = ttk.Label()
labeltext2.grid(padx=0, pady=0, row=9, columnspan=5)

# labeltext3 = ttk.Label()
# labeltext3.config(text="Свободные кабинеты:")
# labeltext3.grid(padx=0, pady=0, row=10, column=1)
#
# labelfloor4 = ttk.Label()
# labelfloor4.grid(padx=0, pady=0, row=11, columnspan=5, column=1)
#
# labelfloor3 = ttk.Label()
# labelfloor3.grid(padx=0, pady=0, row=12, columnspan=5, column=1)
#
# labelfloor2 = ttk.Label()
# labelfloor2.grid(padx=0, pady=0, row=13, columnspan=5, column=1)
#
# labelfloor1 = ttk.Label()
# labelfloor1.grid(padx=0, pady=0, row=14, columnspan=5, column=1)



labelid = ttk.Label()
labelid.config(text="Номер записи", width=13)
labelid.grid(padx=0, pady=0, row=7, column=4)

entryid = ttk.Entry()
entryid.config(width=9)
entryid.grid(padx=3, pady=6, row=8, column=4)

root.mainloop()

connection.commit()
connection.close()
