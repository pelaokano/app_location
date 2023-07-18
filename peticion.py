import requests
import json
import csv
import time

url = f"http://192.168.0.164:8000/recibir"
payload = ""

datos=None
with open('ubicaciones.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    datos = [l for l in csv_reader]

for l in datos:
    print(l[0])
    print(l[1])
    print(l[2])

    ubicaciones = {"longitud":f"{str(l[1])}",
                   "latitud":f"{str(l[0])}",
                   "direccion":f"{str(l[2])}"}
    
    response = requests.request("POST", url, json=ubicaciones)
    print(response.status_code)
    time.sleep(3)


