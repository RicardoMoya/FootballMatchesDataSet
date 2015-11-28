# -*- coding: utf-8 -*-
__author__ = 'Richard'

import ScrapBDFutbol as bdFutbol
import ScrapTemporada2015 as thisTemporada

# Guardo los partidos de futbol en un diccionario
partidos = dict()

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bdFutbol.getPartidos()

# Obtengo los partidos de futbol de la temporada presente
partidos2015_16 = thisTemporada.getPartidos(bdFutbol.getContador())



file = open('DataSetPartidos.txt','w')
for key,value in partidos.items():
    file.write('%s\n' %str(value))

for key,value in partidos2015_16.items():
    file.write('%s\n' %str(value))

file.close()