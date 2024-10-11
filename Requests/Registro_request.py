# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:41:04 2024

@author: ijrios
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
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

pd.options.mode.chained_assignment = None

opc = webdriver.ChromeOptions()

opc.add_argument("--no-sandbox")
opc.add_argument("--disable-dev-shm-usage")
opc.add_argument("--disable-gpu")
opc.add_argument("--disable-blink-features=AutomationControlled")
opc.add_argument("--start-maximized")
# opc.add_argument("--window-size=1920x1080")
opc.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
opc.add_argument("--ignore-certificate-errors")
opc.add_argument("--allow-running-insecure-content")
opc.add_argument("--disable-notifications")
opc.add_argument("--disable-blink-features")
# opc.add_argument("--incognito")
opc.add_argument('--no-proxy-server')
opc.add_argument("--proxy-server='direct://'")
opc.add_argument("--proxy-bypass-list=*")
opc.add_argument('--disable-dev-shm-usage')
opc.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
opc.add_experimental_option('useAutomationExtension', False)
opc.add_experimental_option("excludeSwitches", ["enable-automation"])
opc.add_argument("disable-infobars")
prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
opc.add_experimental_option("prefs", prefs)


site_url ='https://coleyco.sharepoint.com/sites/Automatizaciones/Registro%20marcas'
ctx = ClientContext(site_url).with_credentials(UserCredential("e2consultoria@cole-coabogados.com", "Automations.0"))

#Credenciales
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
site_url = os.getenv('SITE_URL')
document_library = os.getenv('DOCUMENT_LIBRARY')

# Función para ingresar texto a las inputs
def IngresarTexto(xpath, texto):
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,xpath,)))\
        .send_keys(texto)

# Función para hacer clic en elementos
def Click(xpath):
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH, xpath)))\
        .click()
        
# Función para limpiar los inputs antes de ingresar texto
def LimpiarCampos(xpath):
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,xpath,)))\
        .clear()
    

try:
    def dataframeSP(lista):
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()

        sp_list = lista
        sp_lists = ctx.web.lists
        s_list = sp_lists.get_by_title(sp_list)
        all_items = []
        query = s_list.items

        while True:
            items_to_load = query.get().top(5000)
            ctx.load(items_to_load)
            ctx.execute_query()
            all_items.extend(items_to_load)
            if len(items_to_load) < 5000:
                break
            query = s_list.items.skip(len(all_items)) 

        if all_items:
            columnas = list(all_items[0].properties.keys())
            valores = [list(item.properties.values()) for item in all_items]
            resultado = pd.DataFrame(valores, columns=columnas)
            resultado.set_index("Id", inplace=True)
        else:
            resultado = pd.DataFrame() 

        return resultado
    
except:
    print("No hay datos")

dfRegistroMarca = dataframeSP("Marcas")
dfClases = dataframeSP("Clase_Items")

#idS = sys.argv[1]
idS = 1772

try:
    df = dfRegistroMarca.query(f"Id == {idS}")
    row = json.loads(df.iloc[0].to_json())
    
except:
    print("El id proporcionado es invalido verifique e intente nuevamemente")
    quit()
    
clases = []

# Obtención de elementos asociados (clases)
for _ , clase in dfClases.iterrows():
    if clase["IWParentLink"]:
        print( clase["IWParentLink"]["Url"].split("ID=")[1])
        if str(clase["IWParentLink"]["Url"].split("ID=")[1]) == str(idS):
            print( clase["IWParentLink"]["Url"].split("ID=")[1])
            clases.append({"numero":clase["Numero"], "productosservicios":clase["Clase"]})
            print( clase["Clase"])

# Asignación de variables con la información para la SIPI
for row, datos in df.iterrows():
    referencia = datos['Referencia']
    identidad = datos['EstoyActuando']
    idCliente = datos['Identificacion']
    cliente = datos['Nombre']
    cliente_upper = datos['Nombre'].upper()
    tipoSigno = datos['SignoDistintivo']
    naturaleza = datos['Tipo']
    denominacion = datos['Denominacion']
    reivindicacion = datos['ColoresReivindicacion']
    descReivindicacion = datos['DescripcionReivindicacion']
    alcance = datos['Alcance']
    transliteracion = datos['Transliteracion']
    poder = datos['Poder']
    numeroFolios = datos['NumeroFolios']
    

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

cliente_folder_name = cliente.replace(' ', '_')
denominacion_folder_name = denominacion.replace(' ', '_')

def verificar_carpeta_duo(base_folder, denominacion):
    carpeta_cliente = base_folder.folders.get_by_url(denominacion)
    ctx.load(carpeta_cliente)
    try:
        ctx.execute_query()
        print(f"La carpeta '{denominacion}' existe.")
        return carpeta_cliente
    except Exception as e:
        print(f"La carpeta '{denominacion}' no existe.")
        return None

def verificar_carpeta(padre, nombre_carpeta):
    try:
        carpeta = padre.folders.get_by_url(nombre_carpeta)
        ctx.load(carpeta)
        ctx.execute_query()
        return carpeta
    except Exception as e:
        return None
    
def descargar_ultimo_archivo(carpeta, extensiones_permitidas=[".png", ".jpg"]):
    ctx.load(carpeta.files)
    ctx.execute_query()
    
    for file in carpeta.files:
        print(f"Archivo disponible: {file.properties['Name']}")
    
    files = [f for f in carpeta.files if os.path.splitext(f.properties["Name"])[1].lower() in extensiones_permitidas]
    
    if files:
        ultimo_archivo = files[-1]
        file_content = bytearray()
        file_name = ultimo_archivo.properties["Name"]
        ruta_temporal = f"C:/Users/Usuario/Documents/Coleyco/RegistroMarca/temporal/{file_name}"
        
        with io.BytesIO() as output:
            ultimo_archivo.download(output)
            ctx.execute_query()
            # Guardar archivo en ruta temporal
            with open(ruta_temporal, "wb") as file:
                file.write(output.getvalue())
            print(f"Archivo '{file_name}' descargado correctamente en {ruta_temporal}")
        return ruta_temporal
    else:
        print("No se encontraron archivos PNG o JPG en la carpeta.")
        return None

base = ctx.web.lists.get_by_title("Documentos")
ctx.load(base)
ctx.execute_query()

cliente_folder_name = str(cliente).replace(' ', '_').replace('.', '_')
denominacion_folder_name = str(denominacion).replace(' ', '_')
carpeta_cliente = verificar_carpeta(base.root_folder, cliente_folder_name)
if carpeta_cliente:
    print(f"La carpeta '{cliente_folder_name}' existe.")
    carpeta_denominacion = verificar_carpeta(carpeta_cliente, denominacion_folder_name)
    if carpeta_denominacion:
        
        ctx.load(carpeta_denominacion.files)
        ctx.execute_query()
        files = carpeta_denominacion.files
        ctx.load(files)
        ctx.execute_query()
        
        def definePathFile(name_file):
            folder = r"C:/Users/Usuario/Documents/Coleyco/RegistroMarca/temporal/"
            name, extension = os.path.splitext(name_file)
            return folder+"poder"+extension


        locationFile = ""
        
        if files:
            first_file = files[0]
            file_content = bytearray()
            with io.BytesIO() as output:
                locationFile = definePathFile(first_file.properties["Name"])
                with open(locationFile, "wb") as file:
                    first_file.download(output)
                    ctx.execute_query()
                    file.write(output.getvalue())
            print("Descargado correctamente")
        else:
            print("No hay ni mierda")
            
            
        print(f"La carpeta '{denominacion_folder_name}' existe.")
    
    else:
        print(f"La carpeta '{denominacion_folder_name}' no existe dentro de '{cliente_folder_name}'.")
else:
    print(f"La carpeta '{cliente_folder_name}' no existe.")

carpeta_cliente_duo = verificar_carpeta_duo(ctx.web.get_folder_by_server_relative_url(document_library), denominacion)
if carpeta_cliente_duo:
    print(f"La carpeta '{denominacion}' existe.")
    if carpeta_cliente_duo:
        
        ctx.load(carpeta_cliente_duo.files)
        ctx.execute_query()
        files = carpeta_cliente_duo.files
        ctx.load(files)
        ctx.execute_query()

        def definePathFile(name_file):
            folder = r"C:/Users/Usuario/Documents/Coleyco/RegistroMarca/temporal/"
            name, extension = os.path.splitext(name_file)
            return folder+"ilustracion"+extension


        locationFile_duo = ""
        
        if files:
            first_file = files[0]
            file_content = bytearray()
            with io.BytesIO() as output:
                locationFile_duo = definePathFile(first_file.properties["Name"])
                with open(locationFile_duo, "wb") as file:
                    first_file.download(output)
                    ctx.execute_query()
                    file.write(output.getvalue())
            print("Descargado correctamente")
        else:
            print("No hay ni mierda")
            
            
        print(f"La carpeta '{denominacion}' existe.")
    
    else:
        print(f"La carpeta '{denominacion}' no existe dentro de '{denominacion}'.")
else:
    print(f"La carpeta '{denominacion}' no existe.")
    

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
            'X-MicrosoftAjax': 'Delta=true',
            'X-Requested-With': 'XMLHttpRequest',
        }
         
    return headers_final
   

session = requests.Session()  

# URL de inicio de sesión
login_url = 'https://sipi.sic.gov.co/sipi/Extra/Entity/User/Login.aspx?sid='
base_url = 'https://sipi.sic.gov.co/sipi/Extra/Default.aspx'
baseGet = session.get(base_url, allow_redirects=True)
idTransaction = baseGet.url.split("?sid=")[1]
base_url = base_url+'?sid='+idTransaction

path =r"C:\driver\chromedriver\win64\chromedriver.exe"
service = Service(path)
driver = webdriver.Chrome(service=service)
action = ActionChains(driver)

driver.get(base_url)
time.sleep(5)

login_text = os.getenv('LOGIN_TEXT')
#Inicio de sesión
Click('/html/body/div[1]/form/div[3]/div[2]/div/div/div[2]/a[2]')
time.sleep(2)
IngresarTexto('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/table/tbody/tr[1]/td[2]/input', login_text)
time.sleep(2)
IngresarTexto('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]/td[2]/input', login_text)
time.sleep(2)
Click('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/div/a[1]')
time.sleep(2)


elemento = driver.find_element(By.XPATH, "/html/body/div[1]/form/div[4]/div/table/tbody/tr/td[1]/h3[2]")

wait = WebDriverWait(driver, 10) 
radio_button = wait.until(EC.presence_of_element_located((By.ID, 'SidebarContent_SidebarExtra_hdrTM_lblheader')))
radio_button.click()
time.sleep(10)

wait = WebDriverWait(driver, 10) 
radio_button = wait.until(EC.presence_of_element_located((By.ID, 'SidebarContent_SidebarExtra_lnkTMKeyin')))
radio_button.click()
time.sleep(4)

wait = WebDriverWait(driver, 10)  
radio_button = wait.until(EC.presence_of_element_located((By.ID, 'SidebarContent_SidebarExtra_popup_lnkBtnCancel')))
radio_button.click()
time.sleep(2)

cookies_unus = driver.get_cookies()
cookies = {
    'ASP.NET_SessionId': '',
    'selectedCulture': '',
    'cookiesession1': ''
}

for cookie in cookies_unus:
    if cookie['name'] in cookies:
        cookies[cookie['name']] = cookie['value']

current_url = driver.current_url
idsid = current_url.split("?sid=")[1] if "?sid=" in current_url else None

print("Cookies:", cookies)
print("ID Sid:", idsid)

url_form= f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Keyin.aspx?sid={idsid}'

if identidad == 'En nombre propio':
    if naturaleza == "Nominativa":
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        print("Estado de la respuesta Solicitud':", response_form.status_code)
        soup = BeautifulSoup(response_form.text, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']

        datae = {
            'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            'ctl00$selectedCulture': '',
            'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
            'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$txtReference': referencia,
            'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '0',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$gvCustomers$ctl04$ctl08': '-1',
            'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1', 
            'ctl00$MainContent$ctrlTMEdit$ddlType': '1', 
            'ctl00$MainContent$ctrlTMEdit$txtDenomination':denominacion,
            'ctl00$MainContent$ctrlTMEdit$txtMarkDesc': '',
            'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
            'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
            'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
            'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
            #'ctl00$ctl10': '638638914729280412',
            #'scrollY': '500',
            '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            'sid': idsid
        }

        response_datae = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=datae)
        content=response_datae.text
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        
        time.sleep(2)

        # FINAL PARA GUARDAR 
        url_final = f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Keyin.aspx?sid={idsid}'

        data_final = {
            "__EVENTTARGET": "ctl00$MainContent$ctrlSaveAppConfirm$lnkBtnAccept",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$hcSaveApp$hfCollapsed": "",
            "ctl00$MainContent$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$txtReference": referencia,
            "ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity": "0", 
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08": "-1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ddlMarkNature": "1", #marca
            "ctl00$MainContent$ctrlTMEdit$ddlType": "1", #nominativa
            "ctl00$MainContent$ctrlTMEdit$txtDenomination": denominacion,
            "ctl00$MainContent$ctrlTMEdit$rbtnColor": "0",
            "ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition": "",
            "ctl00$MainContent$ctrlTMEdit$txtDisclaimer": "",
            "ctl00$MainContent$ctrlTMEdit$txtTransliteration": transliteracion,
            "ctl00$MainContent$ctrlTMEdit$txtTranslation": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname": "",
            "ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$ctrlExportResult$tbEmail": "notificaciones@cole-coabogados.com",
            #"ctl00$ctl10": "638636500780681621",
            'sid': idsid
        }

        response_final= requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_final)
        print("Estado de la respuesta final':", response_final.status_code)
        time.sleep(2)


    elif naturaleza == "Mixta" or naturaleza == "Figurativa":
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        print("Estado de la respuesta Solicitud':", response_form.status_code)
        soup = BeautifulSoup(response_form.text, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        
        type_natural = ''

        if naturaleza == "Mixta":
            type_natural = '3'
          
        elif naturaleza == "Figurativa":
            type_natural = '2'

        datae = {
                'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
                'ctl00$selectedCulture': '',
                'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
                'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
                'ctl00$MainContent$txtReference': referencia,
                'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
                'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '0',
                'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$gvCustomers$ctl04$ctl08': '-1',
                'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
                'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
                'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
                'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1',
                'ctl00$MainContent$ctrlTMEdit$ddlType': type_natural,
                'ctl00$MainContent$ctrlTMEdit$txtDenomination':denominacion,
                'ctl00$MainContent$ctrlTMEdit$txtMarkDesc': '',
                'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
                'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
                'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
                'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
                'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
                'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
                'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
                'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
                #'ctl00$ctl10': '638638914729280412',
                #'scrollY': '500',
                '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                'sid': idsid
            }
           

        response_datae = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=datae)
        content=response_datae.text
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        
        time.sleep(2)

        #SUBIMO EL LOGOTIPO - ILUSTRACION
        dataLogo = {
        'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$upDocGrid|ctl00$MainContent$ctrlTMEdit$ctrlPictureList$lnkbtnAddDocument',
        'ctl00$selectedCulture': '',
        'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
        'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
        'ctl00$MainContent$txtReference': referencia,
        'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '0',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08': '-1',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference': '',
        'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1',
        'ctl00$MainContent$ctrlTMEdit$ddlType': type_natural,
        'ctl00$MainContent$ctrlTMEdit$txtDenomination': denominacion,
        'ctl00$MainContent$ctrlTMEdit$rbtnColor': '0',
        'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition': '',
        'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
        'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
        'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
        'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
        'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
        #'ctl00$ctl10': '638641689164764778',
        'scrollY': '1446',
        '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$lnkbtnAddDocument',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        #'__VIEWSTATE': 'BiVI3xEpVWSE',
        #'__VIEWSTATEGENERATOR': '6ABE416E',
        '__VIEWSTATEENCRYPTED': '',
        '__ASYNCPOST': 'true',
     }

        response_logo = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=dataLogo)
        print("Estado de la respuesta logotipo':", response_logo.status_code)
        response_redir = response_logo.text.split('pageRedirect||')[1].split('|')[0]
        response_redir = urllib.parse.unquote(response_redir)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response = requests.get(response_redir, cookies=cookies, headers=headers_general(url_form))
        content_poder = redirect_response.text

        soup_logo= BeautifulSoup(redirect_response.text, 'html.parser')
        viewstate_logo= soup_logo.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator_logo = soup_logo.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100_logo = soup_logo.find('input', {'name': 'ctl00$ctl10'})['value']
        

        url_logo = f'https://sipi.sic.gov.co/sipi/Extra/Entity/Document/Keyin.aspx?sid={idsid}'

        with open(locationFile_duo, 'rb') as f:
            binary_file_duo = f.read()

        # Parámetros del formulario
        data_logo = {
            "__EVENTTARGET": "ctl00$masterNavigation$btnAccept",
            "__EVENTARGUMENT": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$ctrlDocumentEdit0nputFile": binary_file_duo,  # Archivo en formato binario
            "ctl00$ctl10": ct100_logo,
            '__VIEWSTATEGENERATOR': viewstategenerator_logo,
        '__VIEWSTATE': viewstate_logo,
        }

        response_logo_duo = requests.post(url_logo, cookies=cookies, headers=headers_general(url_logo), data=data_logo)
        print("Estado de la respuesta logotipo':", response_logo.status_code)
        response_redir = response_logo_duo.text.split('pageRedirect||')[1].split('|')[0]
        response_redir = urllib.parse.unquote(response_redir)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response = requests.get(response_redir, cookies=cookies, headers=headers_general(url_logo))
        content_poder = redirect_response.text
        time.sleep(2)

        # FINAL PARA GUARDAR 
        url_final = f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Keyin.aspx?sid={idsid}'

        data_final = {
            "__EVENTTARGET": "ctl00$MainContent$ctrlSaveAppConfirm$lnkBtnAccept",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$hcSaveApp$hfCollapsed": "",
            "ctl00$MainContent$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$txtReference": referencia,
            "ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity": "0",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08": "-1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ddlMarkNature": "1", #marca
            "ctl00$MainContent$ctrlTMEdit$ddlType": type_natural, 
            "ctl00$MainContent$ctrlTMEdit$txtDenomination": denominacion,
            "ctl00$MainContent$ctrlTMEdit$rbtnColor": "0",
            "ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition": "",
            "ctl00$MainContent$ctrlTMEdit$txtDisclaimer": "",
            "ctl00$MainContent$ctrlTMEdit$txtTransliteration": transliteracion,
            "ctl00$MainContent$ctrlTMEdit$txtTranslation": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname": "",
            "ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$ctrlExportResult$tbEmail": "notificaciones@cole-coabogados.com",
            #"ctl00$ctl10": "638636500780681621"
        }

        response_final= requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_final)
        print("Estado de la respuesta final':", response_final.status_code)
        time.sleep(2)

# COMO APODERADO
elif identidad == 'Como apoderado':

    if naturaleza == "Nominativa":
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        print("Estado de la respuesta Solicitud':", response_form.status_code)
        soup = BeautifulSoup(response_form.text, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']

        datae = {
            'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            'ctl00$selectedCulture': '',
            'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
            'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$txtReference': referencia,
            'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '1',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$gvCustomers$ctl04$ctl08': '-1',
            'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1',
            'ctl00$MainContent$ctrlTMEdit$ddlType': '1',
            'ctl00$MainContent$ctrlTMEdit$txtDenomination':denominacion,
            'ctl00$MainContent$ctrlTMEdit$txtMarkDesc': '',
            'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
            'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
            'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
            'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
            #'ctl00$ctl10': '638638914729280412',
            #'scrollY': '500',
            '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            'sid': idsid
        }

        response_datae = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=datae)
        content=response_datae.text
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        
        time.sleep(2)

        # FINAL PARA GUARDAR 
        url_final = f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Keyin.aspx?sid={idsid}'

        data_final = {
            "__EVENTTARGET": "ctl00$MainContent$ctrlSaveAppConfirm$lnkBtnAccept",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$hcSaveApp$hfCollapsed": "",
            "ctl00$MainContent$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$txtReference": referencia,
            "ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity": "1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08": "-1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ddlMarkNature": "1", #marca
            "ctl00$MainContent$ctrlTMEdit$ddlType": "1",
            "ctl00$MainContent$ctrlTMEdit$txtDenomination": denominacion,
            "ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition": "",
            "ctl00$MainContent$ctrlTMEdit$txtDisclaimer": "",
            "ctl00$MainContent$ctrlTMEdit$txtTransliteration": transliteracion,
            "ctl00$MainContent$ctrlTMEdit$txtTranslation": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname": "",
            "ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$ctrlExportResult$tbEmail": "notificaciones@cole-coabogados.com",
            #"ctl00$ctl10": "638636500780681621"
        }

        response_final= requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_final)
        print("Estado de la respuesta final':", response_final.status_code)
        time.sleep(2)
    
    elif naturaleza == "Mixta" or naturaleza == "Figurativa":

        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        print("Estado de la respuesta Solicitud':", response_form.status_code)
        soup = BeautifulSoup(response_form.text, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100 = soup.find('input', {'name': 'ctl00$ctl10'})['value']
        

        type_natural_duo = ''

        if naturaleza == "Mixta":
            type_natural_duo = '3'
          
        elif naturaleza == "Figurativa":
            type_natural_duo = '2'

        datae = {
            'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            'ctl00$selectedCulture': '',
            'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
            'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$txtReference': referencia,
            'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '1',
            'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$gvCustomers$ctl04$ctl08': '-1',
            'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1',
            'ctl00$MainContent$ctrlTMEdit$ddlType': type_natural_duo,
            'ctl00$MainContent$ctrlTMEdit$txtDenomination':denominacion,
            'ctl00$MainContent$ctrlTMEdit$txtMarkDesc': '',
            "ctl00$MainContent$ctrlTMEdit$rbtnColor": "0",
            'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
            'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
            'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
            'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
            'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
            'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
            #'ctl00$ctl10': '638638914729280412',
            #'scrollY': '500',
            '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity$1',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            'sid': idsid,
            #'__VIEWSTATE': viewstate,
            #'__VIEWSTATEGENERATOR': viewstategenerator
        }

        response_datae = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=datae)
        content=response_datae.text
        response_form = requests.get(url_form, cookies=cookies, headers=headers_general(url_form))
        soup = BeautifulSoup(response_form.text, 'html.parser')
        ct100 = soup.find('input', {'name': 'ctl00$ctl10'})['value']
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        time.sleep(2)

        data_customers = {
            'sid': idsid,
            'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$lnkBtnSearch',
            #'#ctl00$ctl10': ct100,
            #'scrollY': '500',
            '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlApplicant$lnkBtnSearch',
            #'__VIEWSTATEGENERATOR': viewstategenerator
        }

        url_search= f'https://sipi.sic.gov.co/sipi/Extra/Entity/Customer/Qbe.aspx?sid={idsid}'

        response_form_duo = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_customers)
       #edirect_url_2 = response_form_duo.text.split('pageRedirect||')[1].split('|')[0]
        #redirect_url_2 = urllib.parse.unquote(redirect_url_2)
        # Hacer un nuevo request a la URL de redireccionamiento
        #redirect_response = requests.get(redirect_url_2, cookies=cookies, headers=headers_general(url_form))
        #content_2=redirect_response.text
        #time.sleep(2)
        #print("Estado de la respuesta cliente':", response_form_duo.status_code)
        soup = BeautifulSoup(response_form_duo.text, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        #iewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100 = soup.find('input', {'name': 'ctl00$ctl10'})['value']

        data_customer_search = {
        'ctl00$ScriptManager': 'ctl00$ScriptManager|ctl00$MainContent$ctrlCustomerSearch$lnkbtnSearch',
        '__EVENTTARGET': 'ctl00$MainContent$ctrlCustomerSearch$lnkbtnSearch',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$selectedCulture':'' ,
        'ctl00$MainContent$ctrlCustomerSearch$hdrCriteria$hfCollapsed': '',
        'ctl00$MainContent$ctrlCustomerSearch$ddlType': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$tbName': cliente_upper,
        'ctl00$MainContent$ctrlCustomerSearch$ddlIdType': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$tbCodeNr': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbPhone': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbMobile': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbEmail': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbAddress': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbZipCode': '',
        'ctl00$MainContent$ctrlCustomerSearch$ddlCountry': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlRegion': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlCity':'-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlTyProfile': '-1',
        'sid': idsid,
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator
        }
        response_search = requests.post(url_search, cookies=cookies, headers=headers_general(url_search), data=data_customer_search)
        content_6=response_search.text
        # Hacer un nuevo request a la URL de redireccionamiento
        print("Estado de la respuesta cliente encontrado':", response_search.status_code)
        time.sleep(2)
        #soup_trio = BeautifulSoup(redirect_response.text, 'html.parser')
        match = re.search(r'__VIEWSTATE\|([^|]+)', response_search.text)
        match_duo = re.search(r'__VIEWSTATEGENERATOR\|([^|]+)', response_search.text)
        #match_trio = re.search(r'ctl00$ctl10\|([^|]+)', response_search.text)

        if match:
            viewstate_value = match.group(1)
            viewstategenerator_value =match_duo.group(1)
            #ct100 = match_trio.group(1)
            #print("Valor de __VIEWSTATE:", viewstate_value)
        else:
            print("No se encontró el valor de __VIEWSTATE")

        data_select_all = {
        'ctl00$ScriptManager': 'ctl00$MainContent$ctrlCustomerSearch$upCustomerList|ctl00$MainContent$ctrlCustomerSearch$ctrlCustomerList$gvCustomers$ctl04$ctl03',
        'ctl00$selectedCulture': '',
        'ctl00$MainContent$ctrlCustomerSearch$hdrCriteria$hfCollapsed': '',
        'ctl00$MainContent$ctrlCustomerSearch$ddlType': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$tbName': cliente_upper,
        'ctl00$MainContent$ctrlCustomerSearch$ddlIdType': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$tbCodeNr': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbPhone': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbMobile': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbEmail': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbAddress': '',
        'ctl00$MainContent$ctrlCustomerSearch$tbZipCode': '',
        'ctl00$MainContent$ctrlCustomerSearch$ddlCountry': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlRegion': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlCity': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ddlTyProfile': '-1',
        'ctl00$MainContent$ctrlCustomerSearch$ctrlCustomerList$gvCustomers$ctl04$ctl08': '-1',
        #'ctl00$ctl10': ct100,
        #'scrollY': '713',
        '__EVENTTARGET': 'ctl00$MainContent$ctrlCustomerSearch$ctrlCustomerList$gvCustomers$ctl04$ctl03',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        'sid': idsid,
        '__VIEWSTATE': viewstate_value,
        '__VIEWSTATEGENERATOR': viewstategenerator_value,
        '__VIEWSTATEENCRYPTED': '',
        '__ASYNCPOST': 'true'
    }
        response_selection_all = requests.post(url_search, cookies=cookies,  headers=headers_general(url_search), data=data_select_all)
        #redirect_url_duo = response_selection_all.text.split('pageRedirect||')[1].split('|')[0]
        #redirect_url_duo = urllib.parse.unquote(redirect_url_duo)
        # Hacer un nuevo request a la URL de redireccionamiento
        #redirect_response_duo = requests.get(redirect_url_duo, cookies=cookies, headers=headers_selection_custormer)
        #content_tris = redirect_response_duo.text
        
        response_update = requests.get(url_search, cookies=cookies,  headers=headers_general(url_search))
        soup_trio = BeautifulSoup(response_update.text, 'html.parser')
        viewstate_value_duo = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator_value_duo = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100 = soup.find('input', {'name': 'ctl00$ctl10'})['value']


        data_selection_custormer = {
            '__EVENTTARGET': 'ctl00$masterNavigation$btnSelect',
            'ctl00$MainContent$ctrlCustomerSearch$ctrlCustomerList$gvCustomers$ctl02$chckbxSelected': 'on',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            'sid': idsid,
            '__VIEWSTATEGENERATOR': viewstategenerator_value_duo
        }
        
        ### Seleccion solicitante
        response_selection_custormer = requests.post(url_search, cookies=cookies, headers=headers_general(url_search), data=data_selection_custormer)
        print("Estado de la respuesta cliente seleccionado':", response_selection_custormer.status_code)
        redirect_url_duo = response_selection_custormer.text.split('pageRedirect||')[1].split('|')[0]
        redirect_url_duo = urllib.parse.unquote(redirect_url_duo)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response_duo = requests.get(redirect_url_duo, cookies=cookies, headers=headers_general(url_search))
        content_tris = redirect_response_duo.text


        # SUBIMO EL PODER
        url_poder = f'https://sipi.sic.gov.co/sipi/Extra/Entity/Document/Keyin.aspx?sid={idsid}'

        with open(locationFile, 'rb') as f:
            binary_file = f.read()

        data_boton_poder = {
            "ctl00$ScriptManager": "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$UpdatePanel1|ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlDocumentList$lnkBtnAdd",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$hcSaveApp$hfCollapsed": "",
            "ctl00$MainContent$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$txtReference":referencia,
            "ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity": "1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08": "-1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ddlMarkNature": "1",
            "ctl00$MainContent$ctrlTMEdit$ddlType":type_natural_duo,
            "ctl00$MainContent$ctrlTMEdit$txtDenomination": denominacion,
            "ctl00$MainContent$ctrlTMEdit$rbtnColor": "0",
            "ctl00$MainContent$ctrlTMEdit$txtMarkDesc": "",
            "ctl00$MainContent$ctrlTMEdit$txtDisclaimer": "",
            "ctl00$MainContent$ctrlTMEdit$txtTransliteration": transliteracion,
            "ctl00$MainContent$ctrlTMEdit$txtTranslation": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname": "",
            "ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$ctrlExportResult$tbEmail": "notificaciones@cole-coabogados.com",
            #"ctl00$ctl10": "638639850392946996",
            #"scrollY": "1070",
            "__EVENTTARGET": "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlDocumentList$lnkBtnAdd",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": ""
        }
       
        response_poder_unus = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_boton_poder)
        response_redir = response_poder_unus.text.split('pageRedirect||')[1].split('|')[0]
        response_redir = urllib.parse.unquote(response_redir)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response = requests.get(response_redir, cookies=cookies, headers=headers_general(url_form))
        content_poder = redirect_response.text
        soup_podert= BeautifulSoup(redirect_response.text, 'html.parser')
        viewstate_poder = soup_podert.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator_poder = soup_podert.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100_poder = soup_podert.find('input', {'name': 'ctl00$ctl10'})['value']
    
        payload = {
        '__EVENTTARGET': 'ctl00$masterNavigation$btnAccept',
        '__EVENTARGUMENT': '',
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$selectedCulture': '',
        'ctl00$MainContent$ctrlDocumentEdit$txtPageNumber': '3',
        '__VIEWSTATEGENERATOR': viewstategenerator_poder,
        '__VIEWSTATE': viewstate_poder,
        'ctl00$MainContent$ctrlDocumentEdit$inputFile': open(locationFile, 'rb'),
        "ctl00$ctl10": ct100_poder,
            }
        
        try:
            response_poder_tris = requests.post(url_poder, cookies=cookies, headers=headers_general(url_poder),data=payload)
            content_duo = response_poder_unus.text
            response_poder_qud = requests.post(url_form, cookies=cookies, headers=headers_general(url_poder))
            response_poder_tris.raise_for_status()  
            print('Código de estado:', response_poder_tris.status_code)
            print('Contenido de la respuesta:', response_poder_tris.text)
        except requests.exceptions.RequestException as e:
            print('Error en la solicitud:', e)
        finally:
            print("archivo subido")

        #SUBIMO EL LOGOTIPO - ILUSTRACION
        dataLogo = {
        'ctl00$ScriptManager': 'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$upDocGrid|ctl00$MainContent$ctrlTMEdit$ctrlPictureList$lnkbtnAddDocument',
        'ctl00$selectedCulture': '',
        'ctl00$MainContent$hcSaveApp$hfCollapsed': '',
        'ctl00$MainContent$HeaderCollapse1$hfCollapsed': '',
        'ctl00$MainContent$txtReference': '',
        'ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity': '1',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08': '-1',
        'ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference': referencia,
        'ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ddlMarkNature': '1',
        'ctl00$MainContent$ctrlTMEdit$ddlType': type_natural_duo,
        'ctl00$MainContent$ctrlTMEdit$txtDenomination': denominacion,
        'ctl00$MainContent$ctrlTMEdit$rbtnColor': '0',
        'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition': '',
        'ctl00$MainContent$ctrlTMEdit$txtDisclaimer': '',
        'ctl00$MainContent$ctrlTMEdit$txtTransliteration': transliteracion,
        'ctl00$MainContent$ctrlTMEdit$txtTranslation': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode': '',
        'ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname': '',
        'ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed': '',
        'ctl00$MainContent$ctrlExportResult$tbEmail': 'notificaciones@cole-coabogados.com',
        #'ctl00$ctl10': '638641689164764778',
        'scrollY': '1446',
        '__EVENTTARGET': 'ctl00$MainContent$ctrlTMEdit$ctrlPictureList$lnkbtnAddDocument',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        #'__VIEWSTATE': 'BiVI3xEpVWSE',
        #'__VIEWSTATEGENERATOR': '6ABE416E',
        '__VIEWSTATEENCRYPTED': '',
        '__ASYNCPOST': 'true',
     }

        response_logo = requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=dataLogo)
        print("Estado de la respuesta logotipo':", response_logo.status_code)
        response_redir = response_logo.text.split('pageRedirect||')[1].split('|')[0]
        response_redir = urllib.parse.unquote(response_redir)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response = requests.get(response_redir, cookies=cookies, headers=headers_general(url_form))
        content_poder = redirect_response.text

        soup_logo= BeautifulSoup(redirect_response.text, 'html.parser')
        viewstate_logo= soup_logo.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator_logo = soup_logo.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        ct100_logo = soup_logo.find('input', {'name': 'ctl00$ctl10'})['value']
        

        url_logo = f'https://sipi.sic.gov.co/sipi/Extra/Entity/Document/Keyin.aspx?sid={idsid}'

        with open(locationFile_duo, 'rb') as f:
            binary_file_duo = f.read()

        # Parámetros del formulario
        data_logo = {
            "__EVENTTARGET": "ctl00$masterNavigation$btnAccept",
            "__EVENTARGUMENT": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$ctrlDocumentEdit0nputFile": binary_file_duo,  # Archivo en formato binario
            "ctl00$ctl10": ct100_logo,
            '__VIEWSTATEGENERATOR': viewstategenerator_logo,
        '__VIEWSTATE': viewstate_logo,
        }

        response_logo_duo = requests.post(url_logo, cookies=cookies, headers=headers_general(url_logo), data=data_logo)
        print("Estado de la respuesta logotipo':", response_logo.status_code)
        response_redir = response_logo_duo.text.split('pageRedirect||')[1].split('|')[0]
        response_redir = urllib.parse.unquote(response_redir)
        # Hacer un nuevo request a la URL de redireccionamiento
        redirect_response = requests.get(response_redir, cookies=cookies, headers=headers_general(url_logo))
        content_poder = redirect_response.text
        time.sleep(2)

        # FINAL PARA GUARDAR 
        url_final = f'https://sipi.sic.gov.co/sipi/Extra/IP/TM/Keyin.aspx?sid={idsid}'

        data_final = {
            "__EVENTTARGET": "ctl00$MainContent$ctrlSaveAppConfirm$lnkBtnAccept",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$selectedCulture": "",
            "ctl00$MainContent$hcSaveApp$hfCollapsed": "",
            "ctl00$MainContent$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$txtReference": referencia,
            "ctl00$MainContent$ctrlTMEdit$headerCustomer$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$rbtnlIdentity": "1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$ctrlAgent$gvCustomers$ctl04$ctl08": "-1",
            "ctl00$MainContent$ctrlTMEdit$ctrlApplicant$txtReference": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderPriority$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$hdrClassif$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$HeaderInfo$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ddlMarkNature": "1", #marca
            "ctl00$MainContent$ctrlTMEdit$ddlType": type_natural_duo, #mixta
            "ctl00$MainContent$ctrlTMEdit$txtDenomination": denominacion,
            "ctl00$MainContent$ctrlTMEdit$rbtnColor": "0",
            "ctl00$MainContent$ctrlTMEdit$ctrlPictureList$hfPosition": "",
            "ctl00$MainContent$ctrlTMEdit$txtDisclaimer": "",
            "ctl00$MainContent$ctrlTMEdit$txtTransliteration": transliteracion,
            "ctl00$MainContent$ctrlTMEdit$txtTranslation": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$hdrCriteria$hfCollapsed": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryCode": "",
            "ctl00$MainContent$ctrlTMEdit$ctrlDOAppliedLocationSearchDialog$ctrlCountrySearch$txtCountryname": "",
            "ctl00$MainContent$ctrlPayment$HeaderCollapse1$hfCollapsed": "",
            "ctl00$MainContent$ctrlExportResult$tbEmail": "notificaciones@cole-coabogados.com",
            #"ctl00$ctl10": "638636500780681621"
        }

        response_final= requests.post(url_form, cookies=cookies, headers=headers_general(url_form), data=data_final)
        print("Estado de la respuesta final':", response_final.status_code)
        time.sleep(2)


