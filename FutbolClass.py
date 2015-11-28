# -*- coding: utf-8 -*-
__author__ = 'Richard'

import time, datetime

class Equipo():

    def __init__(self, idClub, nombre):
        self.idClub = idClub
        self.nombre = nombre

    def __str__(self):
        return "%s - %s" %(self.idClub, self.nombre)


class Partido():

    def __init__(self, idPartido, temporada, jornada, local, visitante, golesLocal, golesVisitante, fecha):
        self.idPartido = idPartido
        self.temporada = temporada
        self.jornada = jornada
        self.local = local
        self.visitante = visitante
        self.golesLocal = golesLocal
        self.golesVisitante = golesVisitante
        self.fecha = fecha
        self.timestamp = time.mktime(datetime.datetime.strptime(fecha, "%d/%m/%Y").timetuple())

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               %(self.idPartido, self.temporada, self.jornada, self.local, self.visitante, self.golesLocal, self.golesVisitante, self.fecha, self.timestamp)


