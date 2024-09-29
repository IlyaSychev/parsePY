import pygrib
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog as fd
import json
import os
#var1_value = entry_var1.get()  # Получаем значение из поля

type = "json"

dir_for_jsons_name = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
current_directory = os.getcwd()
json_path = os.path.join(current_directory, dir_for_jsons_name)
os.makedirs(json_path, exist_ok=True)
grb_folder_name = 'grbs'
grb_path = os.path.join(current_directory, grb_folder_name)

def func_txt():

    grb_file = pygrib.open(f'{grb_path}')
    level_arr = [10, 15, 20, 30, 40, 50, 70]

    for grb in grb_file:
        date_obj = datetime.strptime(f'{grb.validDate}', "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d_%H.%M.%S')
        output_txt = f'{date_obj}.txt'
        date = grb.validDate
        parameter = grb.name
        level = grb.level
        data, lats, lons = grb.data()
        if level in level_arr:
            if parameter == 'U component of wind' or parameter == 'V component of wind':
                with open(output_txt, 'a') as file:
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            file.write(
                                f'Date: {date}, Parameter: {parameter}, Level: {level}, Value: {data[i][j]}, Lat: {lats[i][j]}, Lon: {lons[i][j]}\n'
                            )

    grb_file.close()
    txt_file.close()


def func_json(grb_path):

    grb_file = pygrib.open(f'{grb_path}')
    level_arr = [10, 15, 20, 30]
    result_array = []
    start = True
    print(datetime.now())

    for grb in grb_file:
        date_obj = datetime.strptime(f'{grb.validDate}', "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d_%H.%M.%S')
        output_txt = os.path.join(json_path, f'{date_obj}.json')
        date = grb.validDate
        parameter = grb.name
        unit = grb.units
        level = grb.level
        data, lats, lons = grb.data()
        if level in level_arr and grb.typeOfLevel == "isobaricInhPa":
            if parameter == 'U component of wind' or parameter == 'V component of wind':
                with open(output_txt, 'a') as file:
                    if start == True:
                        file.write("[\n")
                        start = False
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            data_object = {
                                'date': f'{date}',
                                'parameter': f'{parameter}',
                                'level': level, #f'{grb.typeOfLevel}',                            
                                'value': data[i][j],
                                'lat': lats[i][j],
                                'lon': lons[i][j],
                                'unit': unit,
                            }
                            json.dump(data_object, file)
                            file.write(",\n")

    with open(output_txt, 'a') as file:
        file.seek(0, 2)
        size = file.tell()
        file.truncate(size - 3)
        file.write("]\n")

    print(datetime.now())
    grb_file.close()

for filename in os.listdir(grb_path):
    file_path = os.path.join(grb_path, filename)
    func_json(file_path)

"""

def on_run():
    if type == "txt":
        func_txt()
    else:
        func_json()


def callback():
    global grb_path
    grb_path = fd.askopenfilename()


root = tk.Tk()
root.title("Парсинг метеоданных")

tk.Label(root, text="Переменная 1:").grid(row=0, column=0, padx=10, pady=10)
entry_var1 = tk.Entry(root)
entry_var1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Загрузите файл с метеоданными").grid(row=1, column=0, padx=10, pady=10)
upload_button = tk.Button(root, text='Выбрать файл', command=callback)
upload_button.grid(row=1, column=1, padx=10, pady=10)

run_button = tk.Button(root, text="Запустить", command=on_run)
run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

"""

