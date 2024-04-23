import os
import random
from dotenv import load_dotenv
import psycopg2 as psy
from psycopg2 import Error

import pandas as pd

from functools import lru_cache

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def connection_db() -> psy.extensions.connection:
    try:
        conn = psy.connect(DATABASE_URL)
        return conn
    except (Exception, Error) as e:
        print('Error while connecting to PostgreSQL', e)
        return None

def random_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    o = random.randint(30, 100)/100
    return 'rgba({}, {}, {}, {})'.format(r, g, b, o)

def convert_milliseconds(ms):
    segundos, milisegundos = divmod(ms, 1000)
    minutos, segundos = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    return f"{horas}h {minutos} min {segundos} secs"

@lru_cache(maxsize=None)
def get_seasons():
    conn = connection_db()
    cur = conn.cursor()

    cur.execute(
        """
            SELECT * FROM seasons;
        """
    )

    records = cur.fetchall()
    cur.close()
    conn.close()

    records_data = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data.columns = columns

    return records_data


@lru_cache(maxsize=None)
def get_map_data(year):
    conn = connection_db()
    cur = conn.cursor()

    cur.execute(
        """
            SELECT 
                r.year, r.name AS race_name,
                c.lat AS circuit_lat, c.lng AS circuit_lng, c.country as circuit_country,
                re.milliseconds AS race_time_in_milliseconds,
                MAX(re.fastestlapspeed) AS fastest_lap_speed
            FROM races AS r
            JOIN circuits AS c ON r.circuitId = c.circuitId
            JOIN (
                SELECT raceId, milliseconds, fastestlapspeed
                FROM results
                WHERE positionOrder = 1
            ) AS re ON r.raceId = re.raceId
            LEFT JOIN (
                SELECT raceId, MIN(milliseconds) AS milliseconds
                FROM lap_times
                GROUP BY raceId
            ) AS l ON r.raceId = l.raceId
            WHERE r.year = %s
            GROUP BY r.year, race_name, circuit_lat, circuit_lng, circuit_country, race_time_in_milliseconds;
        """, (year,)
    )
    
    records = cur.fetchall()
    cur.close()
    conn.close()

    records_data = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data.columns = columns
    records_data = records_data.sort_values(by='year', ascending=True)

    return records_data

@lru_cache(maxsize=None)
def get_constructors_data(year):
    conn = connection_db()
    cur = conn.cursor()

    cur.execute(
        """
            SELECT 
                race_name, 
                constructor_name, 
                SUM(total_points) OVER(PARTITION BY constructor_name ORDER BY race_date) AS total_points
            FROM (
                SELECT 
                    r.name as race_name, 
                    c.name AS constructor_name, 
                    SUM(rs.points) AS total_points,
                    r.date as race_date
                FROM constructors c
                JOIN results rs ON c.constructorid = rs.constructorid
                JOIN races r ON rs.raceid = r.raceid
                WHERE r.year = %s
                GROUP BY r.name, c.name, r.date
            ) AS subquery
            ORDER BY race_date ASC, total_points DESC;
        """, (year,)
    )

    records = cur.fetchall()
    cur.close()
    conn.close()

    records_data = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data.columns = columns
    records_data['race_name'] = records_data['race_name'].str.replace('Grand Prix', 'GP')
    records_data['total_points'] = records_data['total_points'].astype(int)

    return records_data

@lru_cache(maxsize=None)
def get_sankey_data(year):
    conn = connection_db()
    cur = conn.cursor()

    cur.execute(
        """
            SELECT 
                c.constructorid, c.constructorref, c.name, c.nationality,
                d.surname, SUM(r.points) AS total_points
            FROM constructors c
            JOIN constructor_results ON c.constructorId = constructor_results.constructorId
            JOIN races ON constructor_results.raceId = races.raceId
            JOIN results as r ON constructor_results.raceId = r.raceId AND constructor_results.constructorId = r.constructorId AND r.points > 0
            JOIN drivers as d ON r.driverid = d.driverid
            WHERE races.year >= %s
            GROUP BY c.constructorid, c.constructorref, c.name, c.nationality, d.surname
            ORDER BY total_points DESC
            LIMIT 20;
        """, (year,)
    )

    records = cur.fetchall()
    cur.close()
    conn.close()

    return records

@lru_cache(maxsize=None)
def get_constructor_info(year):
    conn = connection_db()
    cur = conn.cursor()
    
    year = str(year)
    print(year)
    
    cur.execute(
        """
            select 
                c.name, max(r.fastestlapspeed) as speed, c.url
            from results r
            join races ra on r.raceid = ra.raceid
            join constructors c on r.constructorid = c.constructorid
            WHERE ra.year = %s
            GROUP BY r.raceid, c.name, c.url
            ORDER BY speed desc
            LIMIT 1;
        """, (year,)
    )

    records = cur.fetchall()    
    records_data = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data.columns = columns

    cur.execute(
        """
            select 
                c.name, sum(r.position) as wins, c.url
            from results r
            join races ra on r.raceid = ra.raceid
            join constructors c on r.constructorid = c.constructorid
            WHERE ra.year = %s and r.position = 1
            GROUP BY c.name, c.url
            ORDER BY wins desc
            LIMIT 1;
        """, (year,)
    )

    records = cur.fetchall()
    records_data2 = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data2.columns = columns

    cur.execute(
        """
            select 
                c.name, count(s.status_category) as problems, c.url
            from results r
            join races ra on r.raceid = ra.raceid
            join constructors c on r.constructorid = c.constructorid
            join categorize_status() s on r.statusid = s.statusid
            WHERE ra.year = %s and not s.status_category in ('Finished', 'Not finished')
            GROUP BY c.name, c.url
            ORDER BY problems DESC
            LIMIT 1;
        """, (year,)
    )

    records = cur.fetchall()
    records_data3 = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data3.columns = columns

    cur.close()
    conn.close()

    return records_data, records_data2, records_data3