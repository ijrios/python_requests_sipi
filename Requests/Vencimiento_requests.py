
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
    

session = requests.Session()  # Crea una sesión para mantener las cookies entre solicitudes

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

#Inicio de sesión
Click('/html/body/div[1]/form/div[3]/div[2]/div/div/div[2]/a[2]')
time.sleep(2)
IngresarTexto('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/table/tbody/tr[1]/td[2]/input', 'coleyco2019')
time.sleep(2)
IngresarTexto('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]/td[2]/input', 'coleyco2019')
time.sleep(2)
Click('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td/div/div[2]/div/a[1]')
time.sleep(2)

#Navegación hasta la sección
# Esta sección permite hacer un manejo al dropdown del elemento donde esta el enlace para buscar expedientes
elemento = driver.find_element(By.XPATH, "/html/body/div[1]/form/div[4]/div/table/tbody/tr/td[1]/h3[2]")
    
# Obtener la lista de clases del elemento
clases = elemento.get_attribute("class").split()
# Verificar si la clase específica está en la lista
clase_buscada = "collapsed"
if clase_buscada in clases:
    #Navegación hasta la sección
    Click('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td[1]/h3[2]')
        
    Click('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td[1]/ul[2]/li[1]/a')
    time.sleep(2)
else:
    Click('/html/body/div[1]/form/div[4]/div/table/tbody/tr/td[1]/ul[2]/li[1]/a')
    time.sleep(2)


# Definir las cookies, headers y datos para el request
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
    print(soup)
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

    driver.close()
    driver.quit()