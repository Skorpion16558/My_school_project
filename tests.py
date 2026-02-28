import sys
import tkinter as tk
import io, cv2
import base64 as bs
from PIL import Image as im, ImageTk as itk
import numpy as np
import sqlite3 as sq
import pandas as pd
from deepface import DeepFace
import subprocess as sb



def face_verify(image_1, image_2):
    try:
        result_dict = DeepFace.verify(img1_path=image_1, img2_path=image_2)
        return result_dict['verified']
    except Exception as _ex:
        return _ex

def append_faces_bd(image_str, surname, name, surname_ot, age, residence_address):

    base_SqLite3 = sq.connect('../Faces.db')
    c = base_SqLite3.cursor()

    base_read = pd.read_sql_query("SELECT * FROM Focus", base_SqLite3)

    size = len(base_read)
    base_read.loc[size] = [image_str, surname, name, surname_ot, age, residence_address]
    # base_read.loc[size]['Лицо'] = image_str
    # base_read.loc[size]['Фамилия'] = surname
    # base_read.loc[size]['Имя'] = name
    # base_read.loc[size]['Отчество'] = surname_ot
    # base_read.loc[size]['Возраст'] = age
    # base_read.loc[size]['Адрес проживания'] = residence_address
    base_read.to_sql('Focus', base_SqLite3, if_exists='replace', index=False)
    c.close()



def fase_search_in_bd(image_str):
    base_sqlite3 = sq.connect('../Faces.db')
    c = base_sqlite3.cursor()

    base = pd.read_sql_query("SELECT * FROM Focus", base_sqlite3)

    # image_data = image_str
    #
    # image_data = bs.b64decode(image_data.encode('latin1'))
    # image_data = io.BytesIO(image_data)
    # image_data = im.open(image_data)
    # image_data = np.array(image_data)
    # image_data = im.fromarray(image_data)
    # image_data.save("images1.png")
    print(len(base))
    info = []
    for i in range(len(base)):
        data = base.iloc[i]['Лицо']
        image_data1 = bs.b64decode(data.encode('latin1'))
        image_data1 = io.BytesIO(image_data1)
        image_data1 = im.open(image_data1)
        image_data1 = np.array(image_data1)
        image_data1 = im.fromarray(image_data1)
        image_data1.save("images2.png")
        a = 'image.png'
        b = 'images2.png'
        bools = face_verify(a, b)

        if bools:


            info.append(base.iloc[i]['Фамилия'])
            info.append(base.iloc[i]['Имя'])
            info.append(base.iloc[i]['Отчество'])
            info.append(base.iloc[i]['Возраст'])
            info.append(base.iloc[i]['Адрес проживания'])
            return info

    c.close()
    info.append(False)
    return False, False


def check_availability_bd():
    base = sq.connect('../Faces.db')
    c = base.cursor()
    try:
        asd = pd.read_sql_query('SELECT * FROM Focus', base)

    except pd.errors.DatabaseError:
        arr = pd.DataFrame({'Лицо': [],'Фамилия':[], 'Имя':[], 'Отчество':[], 'Возраст':[], 'Адрес проживания':[]})
        arr.to_sql('Focus', base, if_exists='replace', index=False)

    c.close()

#
# base_info = sq.connect('Faces.db')
# c = base_info.cursor()
#
# # arr.loc[0, 'Лицо'] = image_str
#
# # arr.to_sql('Focus', base_info, if_exists='replace', index=False)
# base = pd.read_sql_query("SELECT * FROM Focus", base_info)
#
# asd = base.loc[0]['Лицо']
#


check_availability_bd()

def main(func):


    if func != 'Не удалось найти лицо':

        search = fase_search_in_bd(func)
        if search[0] == False:
            print(search)
            wind = tk.Tk()

            wind.title('Введите данные')
            canvas = tk.Canvas(wind, width=1004, height=502)
            canvas.pack()

            imag = im.open('../фон_проект.jpeg')
            photo = itk.PhotoImage(imag)

            canvas.create_image(0, 0, image=photo, anchor=tk.NW)

            def surnames():

                surname1 = surname.get()
                surname.config(state='disabled')

                def names():
                    name1 = name.get()
                    name.config(state='disabled')

                    def surnames_ot():
                        surname_ot1 = surname_ot.get()
                        surname_ot.config(state='disabled')

                        def ages():
                            age1 = age.get()
                            age.config(state='disabled')

                            def residence_addresses():
                                residence_address1 = residence_address.get()
                                residence_address.config(state='disabled')

                                append_faces_bd(func, surname1, name1, surname_ot1, age1, residence_address1)

                                butten = tk.Button(canvas, text="Завершить", command=sys.exit)
                                canvas.create_window(850, 160, window = butten)

                            canvas.create_text(650, 130, text=f"Адрес проживания: ", font=('Arial', 16),
                                               fill='white')

                            residence_address = tk.Entry(wind)
                            canvas.create_window(800, 130, window=residence_address)
                            btn4 = tk.Button(canvas, text='Ок', command=residence_addresses)
                            canvas.create_window(920, 130, window=btn4)

                        canvas.create_text(650, 100, text=f"Возраст: ", font=('Arial', 16), fill='white')
                        age = tk.Entry(wind)
                        canvas.create_window(800, 100, window=age)
                        btn3 = tk.Button(canvas, text='Ок', command=ages)
                        canvas.create_window(920, 100, window=btn3)

                    canvas.create_text(650, 70, text=f"Отчество: ", font=('Arial', 16), fill='white')
                    surname_ot = tk.Entry(wind)
                    canvas.create_window(800, 70, window=surname_ot)
                    btn2 = tk.Button(canvas, text='Ок', command=surnames_ot)
                    canvas.create_window(920, 70, window=btn2)

                canvas.create_text(650, 40, text=f"Имя: ", font=('Arial', 16), fill='white')
                name = tk.Entry(wind)
                canvas.create_window(800, 40, window=name)
                btn1 = tk.Button(canvas, text='Ок', command=names)
                canvas.create_window(920, 40, window=btn1)

            canvas.create_text(650, 10, text=f"Фамилия: ", font=('Arial', 16), fill='white')
            surname = tk.Entry(wind)
            canvas.create_window(800, 10, window=surname)
            btn = tk.Button(canvas, text='Ок', command=surnames)
            canvas.create_window(920, 10, window=btn)
            wind.mainloop()


        else:
            wis = tk.Tk()
            wis.title('Ваши данные')
            canvas = tk.Canvas(wis, width=1004, height=502)
            canvas.pack()

            imag = im.open('../фон_проект.jpeg')
            photo = itk.PhotoImage(imag)

            canvas.create_image(0, 0, image=photo, anchor=tk.NW)

            canvas.create_text(800, 10, text=f"Фамилия: {search[0]}", font=('Arial', 16), fill='white')
            canvas.create_text(800, 40, text=f"Имя: {search[1]}", font=('Arial', 16), fill='white')
            canvas.create_text(800, 70, text=f"Отчество: {search[2]}", font=('Arial', 16), fill='white')
            canvas.create_text(800, 100, text=f"Возраст:{search[3]}", font=('Arial', 16), fill='white')
            canvas.create_text(800, 130, text=f"Адрес проживания:{search[4]}", font=('Arial', 16), fill='white')
            butten = tk.Button(canvas, text="Завершить", command=sys.exit)
            canvas.create_window(850, 160, window=butten)
            wis.mainloop()
sb.run(['python', 'main_file.py'])
image_path = 'image.png'
image = im.open(image_path)

# Преобразуем изображение в байты
buffered = io.BytesIO()
image.save(buffered, format="PNG")
img_str = bs.b64encode(buffered.getvalue()).decode()

main(img_str)



