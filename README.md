# Football Matches DataSet

Para más información visitar el siguiente enlace:
http://jarroba.com/dataset-resultados-partidos-futbol-prediccion-machine-learning/


Este DataSet de partidos de fútbol de la liga Española de primera y segunda división desde la temporada 1970-71 hasta la temporada actual,
se ha creado con el objetivo de abrir una linea de investigación dentro del mundo del Machine Learning, para el cálculo de predicciones de los
resultados de los partidos de fútbol que se jugarán en el futuro.

La motivación de este proyecto surge como resultado del trabajo final realizo en la asigantura de "Redes Neuronales y Aplicaciones" impartida en el "Master en
Ciencias y Tecnologías de la Computación" de la Universidad Politécnica de Madrid (UPM) en la que creé un sistema experto de predicción de quinielas (1X2),
aplicando diferentes técnica de Machine Learning. Con el objetivo de querer profundizar en este tipo de estudios de predicción de resultados de eventos (en este caso deportivos)
publico este DataSet con el objetivo de crear una comunidad que comparta los estudios y técnicas aplicadas para la predicción de resultados de fútbol.

En la web de http://jarroba.com/ se expondrán y explicarán diferentes técnicas de Machine Learning para la predicción de los resultados de partidos de fútbol y
por supuesto todo aquel que quiera compartir sus técnicas o estudios relativos a este tema, podrá publicarlo en la web respetando siempre su autoria.

## Requisitos
Para mantener el data set de partidos de fútbol actualizo y ejecutar el fichero "Main.py" para scrapear los resultados,
hay que tener instaladas las librerias de "beautifulsoup4" y "requests". Para ello lo podeis instalar a través de pip de la siguiente manera:

```ssh
$ pip install beautifulsoup4
$ pip install requests
```

## Scraping

El Scraping realizado en este proyecto se hace a través de dos fuentes:

1.- http://www.bdfutbol.com/: De esta web se obtienen los resultados de todos los partidos de futbol de las temporadas pasadas (1970-71 hasta 2015-16). Esta web no ofrece los resultados de la presente temporada.

2.- http://www.resultados-futbol.com/: De esta web se obtienen los resultados de los partidos jugados de la presente temporada.

## Ejecución del programa.

Para obtener los resultados de los partidos de fútbol, debéis de ejecutar el script "Main.py". Tras su ejecución se creará un fichero llamado "DataSetPartidos.txt" en el que en cada linea se encontrará
los datos de un partido de fútbol. Cada uno de los datos de un partido de fútbol esta separado por los delimitadores "::". El significado de cada uno de esos datos es el siguiente:

"idPartido::temporada::division::jornada::EquipoLocal::EquipoVisitante::golesLocal::golesVisitante::fecha::timestamp"

Un ejemplo seria el siguiente:

4808::1977-78::1::8::Rayo Vallecano::Real Madrid::3::2::30/10/1977::247014000.0

    - idPartido (4808): Un identificador único de partido.
    - temporada (1977-78): Temporada en la que se jugó el partido
    - division (1): División en la que se jugo el partido (Primera '1', Segunda '2')
    - jornada (8): Jornada en la que se jugó el partido
    - EquipoLocal (Rayo Vallecano): Nombre del Equipo Local
    - EquipoVisitante (Real Madrid): Nombre del Equipo Visitante
    - golesLocal (3): Goles que marcó el equipo local
    - golesVisitante (2): Goles que marcó el equipo visitante
    - fecha (30/10/1977): Fecha en la que se jugó el partido
    - timestamp (247014000.0): Timestamp de la fecha en la que se jugó el partido