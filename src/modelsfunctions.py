import os
import pickle
from dotenv import load_dotenv
import psycopg2 as psy
from psycopg2 import Error

import plotly.express as px

import pandas as pd

from functools import lru_cache

import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import requests

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def connection_db() -> psy.extensions.connection:
    try:
        conn = psy.connect(DATABASE_URL)
        return conn
    except (Exception, Error) as e:
        print('Error while connecting to PostgreSQL', e)
        return None
    
@lru_cache(maxsize=None)
def get_teams(year):
    conn = connection_db()
    cur = conn.cursor()
    cur.execute(
        """
            SELECT 
                DISTINCT c.constructorid, c.name, c.url
            FROM constructors c
            JOIN results r ON c.constructorid = r.constructorid
            JOIN races ra ON r.raceid = ra.raceid
            WHERE ra.year = %s
        """, (year,)
    )
    teams = cur.fetchall()
    teams = pd.DataFrame(teams)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    teams.columns = columns

    cur.close()
    conn.close()
    return teams

@lru_cache(maxsize=None)
def get_circuits_data(year):
    conn = connection_db()
    cur = conn.cursor()
    cur.execute(
        """
            select 
                distinct r.raceid, c.name
            from results r
            join races ra on r.raceid = ra.raceid
            join circuits c on ra.circuitid = c.circuitid
            where ra.year = %s;
        """, (year,)
    )
    inputs = cur.fetchall()
    inputs = pd.DataFrame(inputs)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    inputs.columns = columns

    cur.close()
    conn.close()
    return inputs

@lru_cache(maxsize=None)
def get_inputs_params(year):
    conn = connection_db()
    cur = conn.cursor()
    cur.execute(
        """
            SELECT 
                min(grid) as min_grid, 
                max(grid) as max_grid, 
                min(r.milliseconds) / 60000 as min_minutes,
                max(r.milliseconds) / 60000 as max_minutes,
                min(fastestlapspeed) as min_fastestlapspeed,
                max(fastestlapspeed) as max_fastestlapspeed,
                min(p.stop) as min_pit_stop,
                max(p.stop) as max_pit_stop
            FROM results r
            JOIN races ra ON r.raceid = ra.raceid
            JOIN pit_stops p ON r.raceid = p.raceid
            WHERE ra.year = %s
        """, (year,)
    )
    inputs = cur.fetchall()
    inputs = pd.DataFrame(inputs)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    inputs.columns = columns

    cur.close()
    conn.close()
    return inputs

@lru_cache(maxsize=None)
def get_binary_model():
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/binarylsm.pkl'
    response = requests.get(url)
    model_content = response.content
    log_reg = pickle.loads(model_content)
    
    precision = log_reg['precision']
    recall = log_reg['recall']
    f1 = log_reg['f1']
    auc = log_reg['auc']
    fig_hist = log_reg['fig_hist']
    fig_thresh = log_reg['fig_thresh']
    fig_roc = log_reg['fig_roc']
    fig_cm = log_reg['fig_cm']
    
    return precision, recall, f1, auc, fig_hist, fig_thresh, fig_roc, fig_cm

@lru_cache(maxsize=None)
def get_binary_model_predict(year, circuit, grid, minutes, constructorid, pits, fastestlapspeed):
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/binarylsm.pkl'
    response = requests.get(url)
    model_content = response.content
    log_reg = pickle.loads(model_content)

    
    minutes = float(minutes)

    to_predict = pd.DataFrame({
        'year': [year],
        'raceid': [circuit],
        'grid': [grid],
        'minutes': [minutes],
        'constructorid': [constructorid],
        'pit_stop': [pits],
        'fastestlapspeed': [fastestlapspeed]
    })

    model = log_reg['binarylsm']
    y_hat = model.predict(to_predict)[0]

    return y_hat

@lru_cache(maxsize=None)
def get_svm_model():
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/svm.pkl'
    response = requests.get(url)
    model_content = response.content
    svm = pickle.loads(model_content)
    
    precision = svm['precision']
    recall = svm['recall']
    f1 = svm['f1']
    auc = svm['auc']
    fig_cm = svm['fig_cm']
    fig_acc = svm['fig_acc']
    
    return precision, recall, f1, auc, fig_cm, fig_acc

@lru_cache(maxsize=None)
def get_knn_model():
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/knn.pkl'
    response = requests.get(url)
    model_content = response.content
    knn = pickle.loads(model_content)
    
    precision = knn['precision']
    recall = knn['recall']
    f1 = knn['f1']
    auc = knn['auc']
    fig_cm = knn['fig_cm']
    fig_acc = knn['fig_acc']
    
    return precision, recall, f1, auc, fig_cm, fig_acc

@lru_cache(maxsize=None)
def get_knn_predict(points, init, final, laps, speed, win, stop, ret):
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/knn.pkl'
    response = requests.get(url)
    model_content = response.content
    knn = pickle.loads(model_content)

    to_predict = pd.DataFrame({
        'avgpoints': [points],
        'avginitialpos': [init],
        'avgfinalpos': [final],
        'avglaps': [laps],
        'avgfastestlapspeed': [speed],
        'totalwins': [win],
        'avgstops': [stop],
        'avgretirements': [ret]
    })

    model = knn['model']
    y_hat = model.predict(to_predict)[0]

    return y_hat

@lru_cache(maxsize=None)
def get_svm_predict(points, init, final, laps, speed, win, stop, ret):
    url = 'https://github.com/unfresh25/f1-dashboard/raw/main/src/models/svm.pkl'
    response = requests.get(url)
    model_content = response.content
    svm = pickle.loads(model_content)

    #speed = float(speed)

    to_predict = pd.DataFrame({
        'avgpoints': [points],
        'avginitialpos': [init],
        'avgfinalpos': [final],
        'avglaps': [laps],
        'avgfastestlapspeed': [speed],
        'totalwins': [win],
        'avgstops': [stop],
        'avgretirements': [ret]
    })

    model = svm['model']
    y_hat = model.predict(to_predict)[0]

    return y_hat