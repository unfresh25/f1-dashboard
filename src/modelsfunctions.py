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
def get_pca_data():
    conn = connection_db()
    cur = conn.cursor()
    cur.execute(
        """
            SELECT 
                c.constructorId, c.name,
                ROUND(AVG(res.points), 4) AS avg_points, ROUND(AVG(res.grid), 4) AS avg_grid, 
                ROUND(AVG(res.positionOrder), 4) AS avg_positionOrder, ROUND(AVG(res.laps), 4) AS avg_laps, 
                ROUND(AVG(res.fastestLapSpeed), 4) AS avg_fastestLapSpeed,
                ROUND(AVG(CASE WHEN res.positionOrder = 1 THEN 1 ELSE 0 END), 4) AS avg_wins,
                ROUND(AVG(p.stop), 4) AS avg_stops,
                ROUND(AVG(CASE WHEN sta.status != 'Finished' THEN 1 ELSE 0 END), 4) AS avg_abandonos
            FROM Constructors c
            JOIN Results res ON c.constructorId = res.constructorId
            LEFT JOIN Pit_Stops p ON res.raceId = p.raceId AND res.driverId = p.driverId
            LEFT JOIN Status sta ON res.statusId = sta.statusId
            GROUP BY c.constructorId, c.name;
        """
    )
    pca_data = cur.fetchall()
    pca_data = pd.DataFrame(pca_data)

    columns = []
    for column in cur.description:
        columns.append(column[0])

    pca_data.columns = columns

    cur.close()
    conn.close()
    return pca_data

@lru_cache(maxsize=None)
def get_pca_graph(variables):
    constructor_data = get_pca_data()

    constructor_data = constructor_data.apply(pd.to_numeric, errors='ignore')

    constructor_data = constructor_data.fillna(0)
    constructor_data = constructor_data.apply(lambda x: x.replace([float('inf'), float('-inf')], 0) if x.dtype.kind in 'biufc' else x)

    scaler = StandardScaler()
    constructor_data.iloc[:, 2:10] = scaler.fit_transform(constructor_data.iloc[:, 2:10])

    pca = PCA(n_components=4)
    pca_results = pca.fit_transform(constructor_data.iloc[:, 2:10])

    kmeans = KMeans(n_clusters=4, random_state=123)
    pca_results_df = pd.DataFrame(pca_results, columns=["Dim.1", "Dim.2", "Dim.3", "Dim.4"])

    kmeans_result = kmeans.fit_predict(pca_results_df.iloc[:, :2])

    pca_ind = pd.DataFrame(pca_results_df.iloc[:, :2], columns=["Dim.1", "Dim.2"])
    pca_ind['constructorName'] = constructor_data['name']
    pca_ind['avgWins'] = constructor_data['avg_wins']
    pca_ind['avgPoints'] = constructor_data['avg_points']
    pca_ind['avgAbandonos'] = constructor_data['avg_abandonos']
    pca_ind['cluster'] = kmeans_result

    fig = px.scatter(
        pca_ind, x='Dim.1', y='Dim.2', color='cluster', hover_name='constructorName',
        hover_data={'avgWins': True, 'avgPoints': True, 'avgAbandonos': True, 'cluster': True},
        labels={'Dim.1': 'Primera Dimensión', 'Dim.2': 'Segunda Dimensión'},
        title=f"PCA de Constructores de F1",
        color_continuous_scale='Viridis', size_max=10,
        width=1000
    )
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        margin={'b': 0, 'r': 30, 'l': 30, 't': 30},
        xaxis={'title': 'Primera Dimensión', 'gridcolor': 'rgba(0, 0, 0, 0.0)', 'tickfont': {'color': 'white'}},
        yaxis={'title': 'Segunda Dimensión', 'gridcolor': 'rgba(0, 0, 0, 0.0)', 'tickfont': {'color': 'white'}},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        hoverlabel=dict(
            bgcolor="#111"
        ),
        showlegend = False
    )
    variables_contributions = pca.components_.T * np.sqrt(pca.explained_variance_)

    for i, feature in enumerate(constructor_data.iloc[:, 2:10]):
        fig.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=variables_contributions[i, 0],
            y=variables_contributions[i, 1],
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top",
            font=dict(color="white", size=10)
        )
        fig.add_annotation(
            x=variables_contributions[i, 0],
            y=variables_contributions[i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5,
        )

    kmeans_result = kmeans.fit_predict(pca_results_df.iloc[:, :3])

    pca_ind = pd.DataFrame(pca_results_df.iloc[:, :3], columns=["Dim.1", "Dim.2", "Dim.3"])
    pca_ind['constructorName'] = constructor_data['name']
    pca_ind['avgWins'] = constructor_data['avg_wins']
    pca_ind['avgPoints'] = constructor_data['avg_points']
    pca_ind['avgAbandonos'] = constructor_data['avg_abandonos']
    pca_ind['cluster'] = kmeans_result

    fig2 = px.scatter_3d(
        pca_ind, x='Dim.1', y='Dim.2', z='Dim.3', color='cluster',
        hover_name='constructorName',
        hover_data={'avgWins': True, 'avgPoints': True, 'cluster': False},
        labels={'Dim.1': 'Primera Dimensión', 'Dim.2': 'Segunda Dimensión', 'Dim.3': 'Tercera Dimensión'},
        title=f"3D PCA de Constructores de F1",
        color_continuous_scale='Viridis', size_max=5
    )

    fig2.update(layout_coloraxis_showscale=False)
    fig2.update_layout(
        margin={'b': 0, 'r': 30, 'l': 30, 't': 30},
        xaxis={'title': 'Primera Dimensión', 'gridcolor': 'rgba(0, 0, 0, 0.0)', 'tickfont': {'color': 'white'}},
        yaxis={'title': 'Segunda Dimensión', 'gridcolor': 'rgba(0, 0, 0, 0.0)', 'tickfont': {'color': 'white'}},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        hoverlabel=dict(
            bgcolor="#111"
        ),
        scene=dict(
            xaxis=dict(backgroundcolor='rgba(0, 0, 0, 0)', gridcolor= '#333'),
            yaxis=dict(backgroundcolor='rgba(0, 0, 0, 0)', gridcolor= '#333'),
            zaxis=dict(backgroundcolor='rgba(0, 0, 0, 0)', gridcolor= '#333'),
            bgcolor='rgba(0, 0, 0, 0)',
        ),
        showlegend = False
    )

    return fig, fig2