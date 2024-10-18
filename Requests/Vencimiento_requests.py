# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 20:55:51 2024

@author: Alexander Rios
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from time import localtime, strptime
from datetime import timedelta
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import relativedelta, MO
from time import localtime, strftime
import time
global pagereports
import pandas as pd
import time
import glob
import os
import io
from os.path import exists
import sys
import openpyxl
import warnings
import re
import numpy as np
import calendar
from office365.sharepoint.files.file import File
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from shareplum import Office365, Site
from shareplum.site import Version
import pyautogui
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
import knime
import shutil
import func_timeout
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import json

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None
requests.packages.urllib3.disable_warnings() 
site_url ='https://coleyco.sharepoint.com/sites/Automatizaciones/Registro%20marcas'

#Credenciales
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
site_url = os.getenv('SITE_URL')
document_library = os.getenv('DOCUMENT_LIBRARY')

try:
    ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
except Exception as e:
    print(f"Error al establecer conexión: {e}")


try:
    def dataframeSP(lista):
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()

        sp_list = lista
        sp_lists = ctx.web.lists
        s_list = sp_lists.get_by_title(sp_list)

        # Inicializa la consulta y la lista para almacenar todos los elementos
        all_items = []
        query = s_list.items

        while True:
            # Carga hasta 5000 elementos por solicitud (ajusta según sea necesario)
            items_to_load = query.get().top(5000)
            ctx.load(items_to_load)
            ctx.execute_query()

            # Añade los elementos obtenidos a la lista
            all_items.extend(items_to_load)

            # Si no hay más elementos, termina el bucle
            if len(items_to_load) < 5000:
                break

            # Ajusta el token de paginación para la siguiente consulta
            query = s_list.items.skip(len(all_items))  # Cambia a `skip` para la próxima carga

        # Procesar los elementos recopilados
        if all_items:
            columnas = list(all_items[0].properties.keys())
            valores = [list(item.properties.values()) for item in all_items]
            resultado = pd.DataFrame(valores, columns=columnas)
            resultado.set_index("Id", inplace=True)
        else:
            resultado = pd.DataFrame()  # Devuelve un DataFrame vacío si no hay elementos

        return resultado
    
except:
    print("No hay datos")

    
def formatear_vencimiento(Vencimiento):
    meses = {
        'ene': '01',
        'feb': '02',
        'mar': '03',
        'abr': '04',
        'may': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'sep': '09',
        'oct': '10',
        'nov': '11',
        'dic': '12',
        'sept':'9'
    }
   
    match = re.search(r'(\d{1,2})\s(\w{3})\.\s(\d{4})', Vencimiento)
 
    if match:
        dia = match.group(1)          # '18'
        mes_texto = match.group(2)    # 'jul'
        año = match.group(3)          # '2026'
       
        mes_numero = meses.get(mes_texto)
 
        if mes_numero:
            fecha_formateada = f"{dia}/{mes_numero}/{año}"
            return fecha_formateada
        else:
            print("Mes no válido")
            return None
    else:
        print("Formato de fecha no válido")
        return None
    

def headers_general(url):
    headers_final = {}
    if url is None:
         headers_final = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'sipi.sic.gov.co',
            'Origin': 'https://sipi.sic.gov.co',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Cache-Control': 'no-cache'
        }
         
    return headers_final

def headers_general_duo(url):
    headers_final = {}
    if url is None:
         headers_final = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/html; charset=utf-8',
            'Host': 'sipi.sic.gov.co',
            'Origin': 'https://sipi.sic.gov.co',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Cache-Control': 'no-cache'
        }
         
    return headers_final

session = requests.Session()  

url_default= f'https://sipi.sic.gov.co/sipi/Extra/Default.aspx?'

response_default = session.get(url=url_default, headers=headers_general_duo(url_default))
# Hacer un nuevo request a la URL de redireccionamiento
current_url = response_default.url
idsid = current_url.split("?sid=")[1] if "?sid=" in current_url else None
#idsid = '638640064900536677'
cookies= session.cookies.get_dict()

soup= BeautifulSoup(response_default.text, 'html.parser')
viewstate= soup.find('input', {'id': '__VIEWSTATE'})['value']
viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
ct100 = soup.find('input', {'name': 'ctl00$ctl05'})['value']

# Definir las cookies, headers y datos para el request
print("Cookies:", cookies)
print("ID Sid:", idsid)

url_defaul_post= f'https://sipi.sic.gov.co/sipi/Extra/Default.aspx?sid={idsid}'

data_default_post ={
    '__EVENTTARGET': 'ctl00$MainContent$lnkLogin',
    '__EVENTARGUMENT': '',
    'sid': idsid
}

response_default_login = requests.post(url=url_defaul_post,headers=headers_general_duo(url_defaul_post), data=data_default_post, cookies=cookies)
contect_login_text = response_default_login.text
soup= BeautifulSoup(response_default_login.text, 'html.parser') 
viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
ctl00 = soup.find('input', {'name': 'ctl00$ctl10'})['value']
####### LOGIN #########

data_login = {
    '__LASTFOCUS': '',
    '__EVENTTARGET': 'ctl00$MainContent$lnkBtnLogin',
    '__EVENTARGUMENT': '',
    '__VIEWSTATEENCRYPTED': '',
    'ctl00$selectedCulture': '',
    'ctl00$MainContent$tbLogin': 'coleyco2019',
    'ctl00$MainContent$tbPassword': 'coleyco2019',
    'sid': idsid
}
loginurl = response_default_login.url

# Estando en pagina de LOGIN mandamos datos de autenticacion
response_login = requests.post(url=loginurl,headers=headers_general_duo(loginurl), data=data_login, cookies=cookies)
soup= BeautifulSoup(response_login.text, 'html.parser') 
viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
ctl00 = soup.find('input', {'name': 'ctl00$ctl10'})['value']
url_inbox = response_login.url

data_inbox = {
    '__EVENTTARGET': 'ctl00$SidebarContent$SidebarExtra$lnkTMSearch',
    'ctl00$MainContent$ctrlWFInboxTaskSearch$ddlWFActivity': '-1',
    'ctl00$MainContent$ctrlWFInboxTaskSearch$ctrlExtUserInCharge$ctrlUserSearch$ddlStatus': '1',
    'ctl00$MainContent$ctrlWFInboxTaskSearch$ctrlWFInboxTaskList$gvWFInboxTask$ctl09$ctl08': '-1',
    'ctl00$MainContent$ctrlWFInboxTaskSearch$ctrlWFInboxTaskList$ctrlUserSearchDialog$ctrlUserSearch$ddlStatus': '1',
    'ctl00$MainContent$ctrlDiscussionSearch$ddlDiscussionStatus': '-1',
    'ctl00$MainContent$ctrlDiscussionSearch$ddlDiscussionReadStatus': '2',
    'ctl00$MainContent$ctrlDiscussionSearch$ctrlExtUserInCharge$ctrlUserSearch$ddlStatus': '1',
    'ctl00$MainContent$ctrlDiscussionSearch$ctrlDiscussionList$gvwDiscussions$ctl13$ctl10': '10',
    'ctl00$MainContent$ctrlDiscussionSearch$ctrlDiscussionList$gvwDiscussions$ctl13$ctl11': '-1',
    'ctl00$ctl10': ctl00,
    'sid': idsid
}


response_inbox_unus = session.post(url_inbox, headers=headers_general_duo(url_inbox), data= data_inbox)
soup= BeautifulSoup(response_inbox_unus.text, 'html.parser') 
viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
ctl00 = soup.find('input', {'name': 'ctl00$ctl10'})['value']

time.sleep(10)

idsid = current_url.split("?sid=")[1] if "?sid=" in current_url else None

print("Cookies:", cookies)
print("ID Sid:", idsid)

# Definir la URL del POST request
url = f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Qbe.aspx?sid={idsid}'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'sipi.sic.gov.co',
    'Origin': 'https://sipi.sic.gov.co',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
}

dfRegistroMarca = dataframeSP("Marcas")
dfRegistroMarca=dfRegistroMarca[['ID','NumeroExpediente']]
dfRegistroMarca=dfRegistroMarca[~dfRegistroMarca['NumeroExpediente'].isnull()]

for v,consulta in dfRegistroMarca.iterrows():
    con=consulta['NumeroExpediente']
    # Definir los datos del formulario
    data = {
        'ctl00$ScriptManager': 'ctl00$ScriptManager|ctl00$MainContent$ctrlTMSearch$lnkbtnSearch',
        '__EVENTTARGET': 'ctl00$MainContent$ctrlTMSearch$lnkbtnSearch',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        #'__VIEWSTATEGENERATOR': 'A2A01839',  # Este valor puede cambiar
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$selectedCulture': '',
        'ctl00$MainContent$ctrlTMSearch$hdrCriteria$hfCollapsed': '',
        #'ctl00$MainContent$ctrlTMSearch$txtAppNr': 'SD2022/0057773',  # Variable, cambia el número de aplicación
        'ctl00$MainContent$ctrlTMSearch$txtAppNr': '%s' % con , # Variable, cambia el número de aplicación
        #'ctl00$ctl10': '638628680767672389',  # Este valor puede cambiar
        '__ASYNCPOST': 'true',
    }
    
    time.sleep(3) 
    # Realizar el POST request
    response = requests.post(url, cookies=cookies, headers=headers, data=data)
    time.sleep(3) 
    redirect_url = response.text.split('pageRedirect||')[1].split('|')[0]
    redirect_url = urllib.parse.unquote(redirect_url)
    # Hacer un nuevo request a la URL de redireccionamiento
    time.sleep(3) 
    redirect_response = requests.get(redirect_url, cookies=cookies, headers=headers)
    content=redirect_response.text
    
    soup = BeautifulSoup(content, 'html.parser')
    tabla = soup.find('div', {'id': 'MainContent_ctrlTM_panelCaseData'})
        
    
    estado = tabla.find('span', {'id': 'MainContent_ctrlTM_lblCurrentStatus'})
    if estado is not None:
        estado_text = estado.text
        if estado_text == "Registrada":
            gaceta_number = tabla.find('label', {'for': 'MainContent_ctrlTM_txtJournalNumber'}).find_next('td', class_='data').text.strip()
            vigencia = tabla.find('label', {'for': 'MainContent_ctrlTM_txtDtExpiration'}).find_next('td', class_='data').text.strip()
                    
            print('-----')
            print(con)
            print(gaceta_number)
            print(vigencia)
            formatear_vencimiento(vigencia)
            list_name = "Marcas"
            column_name = "NumGaceta"
            column_name_duo = "Vigencia"
            fechita= formatear_vencimiento(vigencia)

    
            # Carga el elemento de la lista por ID
            list_obj = ctx.web.lists.get_by_title(list_name)
            item = list_obj.get_item_by_id(str(consulta['ID']))
            # Modifica el valor de la columna
            item.set_property(column_name, gaceta_number)
            item.set_property(column_name_duo, fechita)
            # Guarda los cambios en SharePoint
            item.update()
            ctx.execute_query()
            print('done')
            print(estado_text)
        else:
            print("No se encontró el estado en la tabla.")
    else:
        print("No se encontró el estado en la tabla.")

print("Proceso finalizado")