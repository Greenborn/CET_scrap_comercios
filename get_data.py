#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import csv
import json
from bs4 import BeautifulSoup

URL = "https://www.camaraempresaria.org.ar/socios.php?cate=comercio&cate_promo=&promo="

pag = 1
comercios = []
while True:
    url = URL + '&pagina='+str(pag)
    print("haciendo petición a: ", url)
    response = requests.get(url)
    response = response.text

    soup = BeautifulSoup(response, 'html.parser')
    tabla = soup.find(class_="table table1 invoice-table table-striped")

    registros = tabla.find_all('tr')
    if (len(registros) == 0):
        break
    
    reg_pasada = 0
    for reg in registros:
        celdas = reg.find_all('td')
        
        if (len(celdas) == 0):
            continue

        enlace = celdas[3].find("a")
        if (enlace != None):
            enlace = enlace.get("href")
        else:
            enlace = ''

        registro = {
            'empresa':   celdas[0].text,
            'direccion': celdas[1].text,
            'actividad': celdas[2].text,
            'enlace':    enlace
        }
        print(registro)
        comercios.append(registro)
        reg_pasada = reg_pasada + 1 
        print("")

    if (reg_pasada == 0):
        break

    pag = pag + 1

with open('comercios_tandil_cet.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(['EMPRESA', 'DIRECCIÓN', 'ACTIVIDAD', 'ENLACE'])
    for reg in comercios:
        spamwriter.writerow([reg['empresa'], reg['direccion'], reg['actividad'], reg['enlace']])

with open('comercios_tandil_cet.json', 'w') as file:
    json.dump(comercios, file)