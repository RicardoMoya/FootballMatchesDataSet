# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

import ScrapBDFutbol as bd_futbol
import ScrapTemporada2016 as this_temporada

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bd_futbol.get_partidos()

# Obtengo los partidos de futbol de la temporada presente
partidos_2016_17 = this_temporada.get_partidos(bd_futbol.get_contador())

fichero = open('DataSetPartidos.txt', 'w')
for key, value in partidos.items():
    fichero.write('%s\n' % str(value))

for key, value in partidos_2016_17.items():
    fichero.write('%s\n' % str(value))

fichero.close()
