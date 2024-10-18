from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.edge.service import Service

edge_driver_path = r'C:\driver\edgedriver_win64\msedgedriver.exe'
service = Service(executable_path=edge_driver_path)

# Opciones adicionales para Edge
options = EdgeOptions()

# Inicia Edge
driver = webdriver.Edge(service=service, options=options)

# Asegúrate de incluir 'https://' al inicio de la URL
driver.get("https://www.youtube.com")