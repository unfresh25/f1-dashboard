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
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    o = random.randint(30, 100)/100
    return 'rgba({}, {}, {}, {})'.format(r, g, b, o)

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
                l.milliseconds AS general_fastest_lap_time
            FROM races AS r
            JOIN circuits AS c ON r.circuitId = c.circuitId
            JOIN (
                SELECT raceId, milliseconds
                FROM results
                WHERE positionOrder = 1
            ) AS re ON r.raceId = re.raceId
            LEFT JOIN (
                SELECT raceId, MIN(milliseconds) AS milliseconds
                FROM lap_times
                GROUP BY raceId
            ) AS l ON r.raceId = l.raceId
            WHERE r.year > %s;
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
                c.name AS constructor_name, 
                COUNT(DISTINCT r.raceId) AS total_races
            FROM 
                constructors c
            JOIN constructor_results cr ON c.constructorId = cr.constructorId
            JOIN races r ON cr.raceId = r.raceId
            WHERE r.year > %s
            GROUP BY 
                c.name
            ORDER BY 
                total_races DESC;
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
def get_fastest_constructor_data(year):
    conn = connection_db()
    cur = conn.cursor()
    
    year = str(year)
    print(year)
    
    cur.execute(
        """
            SELECT 
                c.constructorid, c.constructorref, c.name, c.nationality,
                d.driverref,
                MAX(r.fastestlapspeed) AS max_fastestlapspeed
            FROM constructors c
            JOIN constructor_results ON c.constructorId = constructor_results.constructorId
            JOIN races ON constructor_results.raceId = races.raceId
            JOIN results as r ON constructor_results.raceId = r.raceId AND constructor_results.constructorId = r.constructorId AND r.points > 0
            JOIN drivers as d ON r.driverid = d.driverid
            WHERE races.year = %s
            GROUP BY c.constructorid, c.constructorref, c.name, c.nationality, d.driverref
            ORDER BY max_fastestlapspeed DESC
            LIMIT 1;
        """, (year,)
    )

    records = cur.fetchall()
    print(records)
    cur.close()
    conn.close()

    records_data = pd.DataFrame(records)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    records_data.columns = columns

    print(records_data)

    return records_data