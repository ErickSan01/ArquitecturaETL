##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: application.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define la aplicación que sirve la UI y la lógica 
#   del componente
#
#-------------------------------------------------------------------------
from src.view.dashboard import Dashboard
from dash import html
import dash_bootstrap_components as dbc
import dash

app = dash.Dash(
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

app.title = "ETL"

dashboard = Dashboard()

app.layout = dashboard.document()

@app.callback(
    dash.dependencies.Output('selected_start_date', 'children'),
    [dash.dependencies.Input('date_select', 'start_date')],)
def get_start_date(value):
    if value:
        return value
    return ""

@app.callback(
    dash.dependencies.Output('selected_end_date', 'children'),
    [dash.dependencies.Input('date_select', 'end_date')],)
def get_end_date(value):
    if value:
        return value
    return ""