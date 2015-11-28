# -*- coding: utf-8 -*-
__author__ = 'Richard'

# En este fichero voy a obtener los resultados de futbol de la temporada 2014-15
# WEB: http://www.resultados-futbol.com

from bs4 import BeautifulSoup
from FutbolClass import Partido
import requests, re
import Const

# Guardo los partidos de futbol con un id
partidos = dict()


# Función para sustituir el nombre de los equipos y unificarlos
def replaceEquipos (str):

    str = str.replace('Atltico', 'Atletico de Madrid')
    str = str.replace('Mlaga', 'Malaga')
    str = str.replace('R. Sociedad', 'Real Sociedad')
    str = str.replace('Celta', 'Celta de Vigo')
    str = str.replace('Crdoba', 'Cordoba')
    str = str.replace('Almera', 'Almeria')
    str = str.replace('Athletic', 'Athletic Club')
    str = str.replace('Alavs', 'Alaves')
    str = str.replace('Legans', 'Leganes')
    str = str.replace('Real Betis', 'Betis')
    str = str.replace('Zaragoza', 'Real Zaragoza')
    str = str.replace('Recreativo', 'Recreativo de Huelva')
    str = str.replace('Sporting', 'Sporting de Gijon')
    str = str.replace('Alcorcn', 'Alcorcon')
    str = str.replace('Racing', 'Racing de Santander')
    str = str.replace('Mirands', 'Mirandes')

    return str



# Obtengo la fecha del partido de fútbol
def getFechaPartido (fechaSucia):

    fecha = re.sub(r'[<](/)?td[^>]*[>]', '', fechaSucia).replace('[','')
    fecha = fecha.split('<br/>')[0].strip()
    fecha = fecha.split(' ')
    meses = {'Ene':'01', 'Feb':'02', 'Mar':'03', 'Abr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Ago':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12', }
    fecha = "%s/%s/20%s" %(fecha[0],meses[fecha[1]], fecha[2])

    return fecha



# Obtengo el nombre del equipo de futbol
def getEquipo (equipoSucio):
    club = equipoSucio.find_all('a')[1].text
    club = re.sub(r'[<](/)?a[^>]*[>]', '', club).replace('</a>','').strip()
    return replaceEquipos(club.encode('ascii', 'ignore').decode('ascii'))



# Obtengo el resultado
def getResultado (resultadoSucio):
    resultado = resultadoSucio.find('a').text
    resultado = re.sub(r'[<](/)?a[^>]*[>]', '', resultado).replace('</a>','').strip()

    if 'x' in resultado:
        return None
    else:
        return resultado.split('-')



# Obtengo los datos de un partido de futbol
def getPartido (trPartido):

    soupTr = BeautifulSoup(trPartido)

    fecha = getFechaPartido(str(soupTr.find_all('td',{'class':'fecha'})))
    local = getEquipo(BeautifulSoup(str(soupTr.find_all('td',{'class':'equipo1'}))))
    visitante = getEquipo(BeautifulSoup(str(soupTr.find_all('td',{'class':'equipo2'}))))
    resultado = getResultado(BeautifulSoup(str(soupTr.find_all('td',{'class':'rstd'}))))

    return {
        "local": local,
        "visitante": visitante,
        "gLocal": resultado[0],
        "gVisitante": resultado[1],
        "fecha": fecha
    }



# Obtengo un listado con los partidos de Fútbol
def findPartidos(tablaPartidos):
    partidosJornada = list()
    soupTabla = BeautifulSoup(tablaPartidos)
    trPartidos = soupTabla.find_all('tr',{'class':'vevent'})

    for tr in trPartidos:
        try:
            partidosJornada.append(getPartido(str(tr)))
        except:
            pass

    return partidosJornada



# Obtengo un diccionario con los partidos de futbol obtenidos de esta temporada
def getPartidos(contador):

    print "****** PROCESANDO TEMPORADA 2014-2015 ******"

    # Obtengo los partidos de primera division
    for i in range(1,Const.MaxJornada1+1):
        # Construyo las URLs
        url = Const.urlPrimera2014 % i
        print "Procesando %s" %url

        # Realizo las peticiones a las URLs
        reqPrimera  = requests.get(url)

        # Paso la request a un objeto BeautifulSoup
        soupPrimera = BeautifulSoup(reqPrimera.text)

        # Obtengo la tabla con los resultado de los partidos de la jornada
        tablaPartidos = str(soupPrimera.find('table',{'id':'tabla1'}))
        partidosJornada = findPartidos(tablaPartidos)
        for part in partidosJornada:
            contador += 1
            partidos[contador] = Partido (contador, Const.temporada2014, i, part['local'], part['visitante'], part['gLocal'], part['gVisitante'], part['fecha'])


    # Obtengo los partidos de segunda division
    for i in range(1,Const.MaxJornada2+1):
        # Construyo las URLs
        url = Const.urlSegunda2014 % i
        print "Procesando %s" %url

        # Realizo las peticiones a las URLs
        reqSegunda  = requests.get(url)

        # Paso la request a un objeto BeautifulSoup
        soupSegunda = BeautifulSoup(reqSegunda.text)

        # Obtengo la tabla con los resultado de los partidos de la jornada
        tablaPartidos = str(soupSegunda.find('table',{'id':'tabla1'}))
        partidosJornada = findPartidos(tablaPartidos)
        for part in partidosJornada:
            contador += 1
            partidos[contador] = Partido (contador, Const.temporada2014, i, part['local'], part['visitante'], part['gLocal'], part['gVisitante'], part['fecha'])

    return partidos
