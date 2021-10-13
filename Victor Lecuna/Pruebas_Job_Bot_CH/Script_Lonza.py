#!/usr/bin/env python
# coding: utf-8

# # Test de extraccion de datos
# ## Utilizare como prueba la pagina Lonza: https://www.lonza.com/careers/job-search para la extraccion de los datos.
# 
# Definimos nuestra URL seed aplicando los criterios de filtrado:
# Seed: https://www.lonza.com/careers/job-search?q=data,%20biotech,%20Biostatistics,%20%20clinical%20research&pg=1&rows=100&job_location_facet_sm=Switzerland%2c+Basel

# In[1]:


# IMPORTAMOS LAS LIBRERIAS QUE VAMOS UTILIZAR

from lxml import html
import requests
import pandas as pd
import datetime
import os # PARA CREAR EL DIRECTORIO


# In[2]:



# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}


# In[3]:



# URL SEED
seed = "https://www.lonza.com/careers/job-search?q=data,%20biotech,%20Biostatistics,%20%20clinical%20research&pg=1&rows=100&job_location_facet_sm=Switzerland%2c+Basel"


# In[4]:


# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(seed, headers=headers)


# In[5]:



respuesta


# In[6]:


# PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.text)


# In[7]:


# PARSEO DE TODOS LOS PUESTOS POR CLASE
list_job_names = parser.find_class('search-result-title')

for job_name in list_job_names:
    text_job_name = job_name.text_content()
    print(text_job_name)

len(list_job_names)


# In[8]:


# PARSEO DE TODOS LOS LOCATIONS POR CLASE
list_locations = parser.find_class('search-result-content')

for location in list_locations:
    text_location = location.text_content()
    print(text_location)

len(list_locations)


# In[9]:


# CONVERTIMOS LOS ELEMENTOS LXML EN STR PARA PODER MANIPULAR LAS LISTAS

list_str_job_names = []
list_str_locations = []

for job_name in list_job_names:
    str_job_name = str(job_name.text_content()) # UTILIZO EL METODO TEXT_CONTENT() PARA TRAER DIRECTAMENTE EL TEXTO
    list_str_job_names.append(str_job_name)

for location in list_locations:
    str_location = str(job_name.text_content()) 
    list_str_locations.append(str_location)
    
    

print(list_str_job_names, len(list_str_job_names))
print()
print(list_str_locations, len(list_str_locations))


# In[10]:


# PARSEO DE TODOS LOS HREF POR EMPLEO

list_links = parser.xpath("//div[@class='col-12 col-lg-6']/a/@href")

url_lonza = "https://www.lonza.com"

list_str_links = []

for link in list_links:
    str_link = str(link) # UTILIZO EL METODO STR PARA CONVERTIR EL ELEMENTO EN STRING Y PODER CONCATENAR LAS VARIABLES
    list_str_links.append(url_lonza + str_link)
    
    
print(list_str_links)
len(list_str_links)


# In[11]:


# CREANDO VARIABLE DE FECHA

date = datetime.date.today()
date


# In[12]:


# CREANDO DATAFRAME CON LOS DATOS RECOPILADOS

lonza_dataframe = pd.DataFrame(data = { "Company": "LONZA",
                                       "Data_Time": date,
                                       "Job_Name": list_str_job_names,
                                       "Location": list_str_locations,
                                       "Links": list_str_links})
lonza_dataframe


# In[13]:


# CREANDO DIRECTORIO CON FECHA DE EJECUCION
# RUTA -> C:\Users\lecun\Dropbox\Mi PC (LAPTOP-URCP74CR)\Desktop\Job_Bot_CH\job_bot_ch\Victor Lecuna\Pruebas_Job_Bot_CH

date_dir = str(datetime.date.today())

if os.path.isdir('C:/Users/lecun/Dropbox/Mi PC (LAPTOP-URCP74CR)/Desktop/Job_Bot_CH/job_bot_ch/Victor Lecuna/Pruebas_Job_Bot_CH/' + date_dir):
    print('La carpeta existe.')
    
else:
     
    directorio = 'C:/Users/lecun/Dropbox/Mi PC (LAPTOP-URCP74CR)/Desktop/Job_Bot_CH/job_bot_ch/Victor Lecuna/Pruebas_Job_Bot_CH/' + date_dir
    
    try:
        os.mkdir(directorio)
        
    except OSError:
        print("La creación del directorio %s falló" % directorio)
        
    else:
        print("Se ha creado el directorio: %s" % directorio)


# In[14]:


# CREANDO ARCHIVO CSV CON EL DATAFRAME

lonza_file = lonza_dataframe.to_csv('C:/Users/lecun/Dropbox/Mi PC (LAPTOP-URCP74CR)/Desktop/Job_Bot_CH/job_bot_ch/Victor Lecuna/Pruebas_Job_Bot_CH/'
                                    + date_dir + '/LONZA_' + date_dir + '.csv')


# In[ ]:




