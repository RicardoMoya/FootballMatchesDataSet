# -*- coding: utf-8 -*-
__author__ = 'Richard'

# En este fichero voy a obtener un historico de partidos de futbol de todas
# las temporadas anteriores a la actual a partir de la web:
# http://www.bdfutbol.com/

from bs4 import BeautifulSoup
from FutbolClass import Partido
import requests, re
import Const


# Guardo los partidos de futbol con un id
partidos = dict()

# Guardo los equipos de futbol con su id y su nombre
equipos = dict()

# Contador de Partidos
contador = 0

# Sustituyo los caracteres especiales de HTML
def replaceHtml (string):
    string = string.replace('&aacute;','a')
    string = string.replace('&Aacute;','A')
    string = string.replace('&agrave;','a')
    string = string.replace('&Agrave;','A')
    string = string.replace('&eacute;','e')
    string = string.replace('&egrave;','e')
    string = string.replace('&Eacute;','E')
    string = string.replace('&Egrave;','E')
    string = string.replace('&iacute;','i')
    string = string.replace('&igrave;','i')
    string = string.replace('&Iacute;','I')
    string = string.replace('&Igrave;','I')
    string = string.replace('&oacute;','o')
    string = string.replace('&ograve;','o')
    string = string.replace('&Oacute;','O')
    string = string.replace('&Ograve;','O')
    string = string.replace('&uacute;','u')
    string = string.replace('&ugrave;','u')
    string = string.replace('&Uacute;','U')
    string = string.replace('&Ugrave;','U')
    string = string.replace('&ntilde;','ñ')

    return string


# Función para sustituir el nombre de los equipos y unificarlos
def replaceEquipos (str):

    str = str.replace('Deportivo de La Coruña', 'Deportivo')
    str = str.replace('Barcelona Atletic', 'Barcelona B')

    return str


# Inserto los equipos nuevos en el diccionario
def findEquipos(strResultados):

    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', strResultados)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";','')
        sp = mat.split('|')

        if not sp[0] in equipos:
            equipos[sp[0]] = replaceHtml(sp[1])



# Obtengo una lista con los partidos de futbol de una temporada
def findPartidos(strPartidos, url):

    global contador

    match = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', strPartidos)
    for mat in match:
        jornada = re.findall(r'SP\[.*?]', mat)
        jornada = jornada[0].replace('SP[','').replace(']','')
        mat = re.sub(r'SP.*?="', '', mat).replace('";','')
        sp = mat.split(' ')
        contador += 1
        partidos[contador] = Partido(contador, url, jornada, replaceEquipos(equipos[sp[1]]), replaceEquipos(equipos[sp[2]]), sp[3], sp[4], sp[0])

    return partidos


# Devuelvo un diccionario con todos los partidos de futbol de todas las temporadas
def getPartidos():

    # Genero las URLS y scrapeo los datos
    for url in Const.temporadas:

        print "****  PROCESANDO TEMPORADA %s ****" %url
        # Construyo las URLs
        urlPrimera = Const.urlPrimera % url
        urlSegunda = Const.urlSegunda % url

        # Realizo las peticiones a las URLs
        reqPrimera  = requests.get(urlPrimera)
        reqSegunda  = requests.get(urlSegunda)

        # Paso la request a un objeto BeautifulSoup
        soupPrimera = BeautifulSoup(reqPrimera.text)
        soupSegunda = BeautifulSoup(reqSegunda.text)

        # Obtengo el div donde estan los datos
        datosPrimera = str(soupPrimera.find('div',{'id':'resultats'}))
        datosSegunda = str(soupSegunda.find('div',{'id':'resultats'}))

        # Obtengo equipos de futbol
        findEquipos(datosPrimera)
        findEquipos(datosSegunda)

        # Obtengo los equipos de futbol
        findPartidos(datosPrimera, url)
        findPartidos(datosSegunda, url)

    return partidos


# Devuelvo el valor del contador
def getContador ():
    return contador