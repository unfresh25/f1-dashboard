import os
import pickle
import random
from dotenv import load_dotenv
import psycopg2 as psy
from psycopg2 import Error

from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix
import statsmodels.formula.api as sm

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

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
    
@lru_cache(maxsize=None)
def get_teams():
    conn = connection_db()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT constructorid, name FROM constructors')
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
def get_binary_model():
    with open('src/models/binarylsm.pkl', 'rb') as archivo:
        log_reg = pickle.load(archivo)
    
    precision = log_reg['precision']
    recall = log_reg['recall']
    f1 = log_reg['f1']
    auc = log_reg['auc']
    fig_hist = log_reg['fig_hist']
    fig_thresh = log_reg['fig_thresh']
    fig_roc = log_reg['fig_roc']
    fig_cm = log_reg['fig_cm']

    model = log_reg['binarylsm']
    #y_hat = model.predict(to_predict)[0]
    
    return precision, recall, f1, auc, fig_hist, fig_thresh, fig_roc, fig_cm

@lru_cache(maxsize=None)
def get_binary_model_predict(grid, minutes, constructorid, pits, fastestlapspeed):
    with open('src/models/binarylsm.pkl', 'rb') as archivo:
        log_reg = pickle.load(archivo)

    minutes = float(minutes)

    to_predict = pd.DataFrame({
        'grid': [grid],
        'minutes': [minutes],
        'constructorid': [constructorid],
        'pit_stop': [pits],
        'fastestlapspeed': [fastestlapspeed]
    })

    print(to_predict.dtypes)
    
    model = log_reg['binarylsm']
    y_hat = model.predict(to_predict)[0]

    return y_hat
