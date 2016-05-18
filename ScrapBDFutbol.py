from bs4 import BeautifulSoup
from FutbolClass import Partido
import requests
import re
import Const

# -*- coding: utf-8 -*-
__author__ = 'Richard'

# En este fichero voy a obtener un historico de partidos de futbol de todas
# las temporadas anteriores a la actual a partir de la web:
# http://www.bdfutbol.com/

# Guardo los partidos de futbol con un id
partidos = dict()

# Guardo los equipos de futbol con su id y su nombre
equipos = dict()

# Contador de Partidos
contador = 0


# Sustituyo los caracteres especiales de HTML
def replace_html(equipo):
    equipo = equipo.replace('&aacute;', 'a')
    equipo = equipo.replace('&Aacute;', 'A')
    equipo = equipo.replace('&agrave;', 'a')
    equipo = equipo.replace('&Agrave;', 'A')
    equipo = equipo.replace('&eacute;', 'e')
    equipo = equipo.replace('&egrave;', 'e')
    equipo = equipo.replace('&Eacute;', 'E')
    equipo = equipo.replace('&Egrave;', 'E')
    equipo = equipo.replace('&iacute;', 'i')
    equipo = equipo.replace('&igrave;', 'i')
    equipo = equipo.replace('&Iacute;', 'I')
    equipo = equipo.replace('&Igrave;', 'I')
    equipo = equipo.replace('&oacute;', 'o')
    equipo = equipo.replace('&ograve;', 'o')
    equipo = equipo.replace('&Oacute;', 'O')
    equipo = equipo.replace('&Ograve;', 'O')
    equipo = equipo.replace('&uacute;', 'u')
    equipo = equipo.replace('&ugrave;', 'u')
    equipo = equipo.replace('&Uacute;', 'U')
    equipo = equipo.replace('&Ugrave;', 'U')
    equipo = equipo.replace('&ntilde;', 'ñ')

    return equipo


# Funcion para sustituir el nombre de los equipos y unificarlos
def replace_equipos(equipo):
    equipo = equipo.replace('Deportivo de La Coruña', 'Deportivo')
    equipo = equipo.replace('Barcelona Atletic', 'Barcelona B')

    return equipo


# Inserto los equipos nuevos en el diccionario
def find_equipos(str_resultados):
    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', str_resultados)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";', '')
        sp = mat.split('|')

        if not sp[0] in equipos:
            equipos[sp[0]] = replace_html(sp[1])


# Obtengo una lista con los partidos de futbol de una temporada
def find_partidos(str_partidos, url):
    global contador

    match = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
    for mat in match:
        jornada = re.findall(r'SP\[.*?]', mat)
        jornada = jornada[0].replace('SP[', '').replace(']', '')
        mat = re.sub(r'SP.*?="', '', mat).replace('";', '')
        sp = mat.split(' ')
        contador += 1
        partidos[contador] = Partido(contador, url, jornada,
                                     replace_equipos(equipos[sp[1]]),
                                     replace_equipos(equipos[sp[2]]), sp[3],
                                     sp[4], sp[0])

    return partidos


# Devuelvo un diccionario con todos los partidos de
# futbol de todas las temporadas
def get_partidos():
    # Genero las URLS y scrapeo los datos
    for url in Const.TEMPORADAS:
        print "****  PROCESANDO TEMPORADA %s ****" % url
        # Construyo las URLs
        url_primera = Const.URL_PRIMERA % url
        url_segunda = Const.URL_SEGUNDA % url

        # Realizo las peticiones a las URLs
        req_primera = requests.get(url_primera)
        req_segunda = requests.get(url_segunda)

        # Paso la request a un objeto BeautifulSoup
        soup_primera = BeautifulSoup(req_primera.text)
        soup_segunda = BeautifulSoup(req_segunda.text)

        # Obtengo el div donde estan los datos
        datos_primera = str(soup_primera.find('div', {'id': 'resultats'}))
        datos_segunda = str(soup_segunda.find('div', {'id': 'resultats'}))

        # Obtengo equipos de futbol
        find_equipos(datos_primera)
        find_equipos(datos_segunda)

        # Obtengo los equipos de futbol
        find_partidos(datos_primera, url)
        find_partidos(datos_segunda, url)

    return partidos


# Devuelvo el valor del contador
def get_contador():
    return contador
