# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

import ScrapBDFutbol as bd_futbol
import ScrapTemporada2018 as this_temporada

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bd_futbol.get_partidos()

# Obtengo los partidos de futbol de la temporada presente
partidos_2017_18 = this_temporada.get_partidos(bd_futbol.get_contador())

fichero = open('DataSetPartidos.txt', 'w')
fichero.write('idPartido::temporada::division::jornada::EquipoLocal::'
              'EquipoVisitante::golesLocal::golesVisitante::fecha::timestamp')
for value in partidos.values():
    fichero.write('%s\n' % str(value))

for value in partidos_2017_18.values():
    fichero.write('%s\n' % str(value))

fichero.close()
