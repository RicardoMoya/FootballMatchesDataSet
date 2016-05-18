import ScrapBDFutbol as bdFutbol
import ScrapTemporada2015 as thisTemporada

# -*- coding: utf-8 -*-
__author__ = 'Richard'

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bdFutbol.get_partidos()

# Obtengo los partidos de futbol de la temporada presente
partidos2015_16 = thisTemporada.get_partidos(bdFutbol.get_contador())

fichero = open('DataSetPartidos.txt', 'w')
for key, value in partidos.items():
    fichero.write('%s\n' % str(value))

for key, value in partidos2015_16.items():
    fichero.write('%s\n' % str(value))

fichero.close()
