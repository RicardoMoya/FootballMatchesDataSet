# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
from FutbolClass import Partido
import requests
import re
import Const

# En este fichero voy a obtener los resultados de futbol de la temporada 2014-15
# WEB: http://www.resultados-futbol.com

# Guardo los partidos de futbol con un id
partidos = dict()


# Funcion para sustituir el nombre de los equipos y unificarlos
def replace_equipos(equipo):
    equipo = equipo.replace('Atletico-Madrid', 'Atletico de Madrid')
    equipo = equipo.replace('Real-Sociedad', 'Real Sociedad')
    equipo = equipo.replace('Celta', 'Celta de Vigo')
    equipo = equipo.replace('Athletic Club-Bilbao', 'Athletic Club')
    equipo = equipo.replace('Athletic-Bilbao', 'Athletic Club')
    equipo = equipo.replace('Real Betis', 'Betis')
    equipo = equipo.replace('Zaragoza', 'Real Zaragoza')
    equipo = equipo.replace('Recreativo', 'Recreativo de Huelva')
    equipo = equipo.replace('Sporting de Gijon-Gijon', 'Sporting de Gijon')
    equipo = equipo.replace('Sporting-Gijon', 'Sporting de Gijon')
    equipo = equipo.replace('Racing', 'Racing de Santander')
    equipo = equipo.replace('Real-Madrid', 'Real Madrid')
    equipo = equipo.replace('Valencia-Cf', 'Valencia')
    equipo = equipo.replace('Ud-Palmas', 'Las Palmas')
    equipo = equipo.replace('Gimnastic-Tarragona', 'Gimnastic de Tarragona')
    equipo = equipo.replace('Ucam-Murcia-C-F', 'UCAM Murcia')
    equipo = equipo.replace('Real-Real Zaragoza', 'Real Zaragoza')
    equipo = equipo.replace('Rayo-Vallecano', 'Rayo Vallecano')
    equipo = equipo.replace('Ad-Alcorcon', 'Alcorcon')
    equipo = equipo.replace('Real-Oviedo', 'Real Oviedo')
    equipo = equipo.replace('Sevilla-B', 'Sevilla Atletico')
    equipo = equipo.replace('Girona-Fc', 'Girona')

    return equipo


# Obtengo la fecha del partido de futbol
def get_fecha_partido(fecha_sucia):
    charts_remove = ['[', '\\n', '\\t']
    fecha = re.sub(r'[<](/)?td[^>]*[>]', '', fecha_sucia)\
        .translate(None, ''.join(charts_remove))
    fecha = fecha.split('<br/>')[0].strip()
    fecha = fecha.split(' ')
    meses = {'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04', 'May': '05',
             'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10',
             'Nov': '11', 'Dic': '12', 'Oc': '10', 'Ee': '01'}
    fecha = "%s/%s/20%s" % (fecha[0], meses[fecha[1]], fecha[2])

    return fecha


# Obtengo el nombre del equipo de futbol
def get_equipo(equipo_sucio):
    club = equipo_sucio.find_all('a')[1].attrs['href'].replace('/', '')
    return replace_equipos(club.strip())


# Obtengo el resultado
def get_resultado(resultado_sucio):
    resultado = resultado_sucio.find('a').text
    resultado = re.sub(r'[<](/)?a[^>]*[>]', '', resultado).replace('</a>',
                                                                   '').strip()
    if 'x' in resultado:
        return None
    else:
        return resultado.split('-')


# Obtengo los datos de un partido de futbol
def get_partido(tr_partido):
    soup_tr = BeautifulSoup(tr_partido, "html.parser")

    fecha = get_fecha_partido(str(soup_tr.find_all('td', {'class': 'fecha'})))
    local = get_equipo(
        BeautifulSoup(str(soup_tr.find_all('td', {'class': 'equipo1'}))))
    visitante = get_equipo(
        BeautifulSoup(str(soup_tr.find_all('td', {'class': 'equipo2'}))))
    resultado = get_resultado(
        BeautifulSoup(str(soup_tr.find_all('td', {'class': 'rstd'}))))

    return {
        "local": local,
        "visitante": visitante,
        "gLocal": resultado[0],
        "gVisitante": resultado[1],
        "fecha": fecha
    }


# Obtengo un listado con los partidos de Futbol
def find_partidos(tabla_partidos):
    partidos_jornada = list()
    soup_tabla = BeautifulSoup(tabla_partidos)
    tr_partidos = soup_tabla.find_all('tr', {'class': 'vevent'})

    for tr in tr_partidos:
        try:
            partidos_jornada.append(get_partido(str(tr)))
        except:
            pass

    return partidos_jornada


# Obtengo un diccionario con los partidos de futbol obtenidos de esta temporada
def get_partidos(contador):
    print "****** PROCESANDO TEMPORADA 2016-2017 ******"

    # Obtengo los partidos de primera division
    for i in range(1, Const.MAX_JORNADAS_1 + 1):
        # Construyo las URLs
        url = Const.URL_PRIMERA_2018 % i
        print "Procesando %s" % url

        # Realizo las peticiones a las URLs
        req_primera = requests.get(url)

        # Paso la request a un objeto BeautifulSoup
        soup_primera = BeautifulSoup(req_primera.text, "html.parser")

        # Obtengo la tabla con los resultado de los partidos de la jornada
        tabla_partidos = str(soup_primera.find('table', {'id': 'tabla1'}))
        partidos_jornada = find_partidos(tabla_partidos)
        for part in partidos_jornada:
            contador += 1
            partidos[contador] = Partido(contador, Const.TEMPORADA_2018, 1, i,
                                         part['local'], part['visitante'],
                                         part['gLocal'], part['gVisitante'],
                                         part['fecha'])

    # Obtengo los partidos de segunda division
    for i in range(1, Const.MAX_JORNADAS_2 + 1):
        # Construyo las URLs
        url = Const.URL_SEGUNDA_2018 % i
        print "Procesando %s" % url

        # Realizo las peticiones a las URLs
        req_segunda = requests.get(url)

        # Paso la request a un objeto BeautifulSoup
        soup_segunda = BeautifulSoup(req_segunda.text)

        # Obtengo la tabla con los resultado de los partidos de la jornada
        tabla_partidos = str(soup_segunda.find('table', {'id': 'tabla1'}))
        partidos_jornada = find_partidos(tabla_partidos)
        for part in partidos_jornada:
            contador += 1
            partidos[contador] = Partido(contador, Const.TEMPORADA_2018, 2, i,
                                         part['local'], part['visitante'],
                                         part['gLocal'], part['gVisitante'],
                                         part['fecha'])

    return partidos
