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
from src.controller.dashboard_controller import DashboardController
from dash import dash_table, html
import dash_bootstrap_components as dbc
import dash
from datetime import date
import time
import pandas as pd

app = dash.Dash(
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

app.title = "ETL"

dashboard = Dashboard()

app.layout = dashboard.document()
start_date_G = ""
end_date_G = ""

@app.callback(
    dash.dependencies.Output('store-data', 'data'),
    [dash.dependencies.Input('date_select', 'start_date')],
    [dash.dependencies.Input('date_select', 'end_date')],
    [dash.dependencies.Input('dropdown-horaS', 'value')],
    [dash.dependencies.Input('dropdown-horaE', 'value')])
def get_start_date(start_date, end_date, valueS, valueE):
    sales_per_date = DashboardController.load_sales_per_date()
    data = []

    for product in sales_per_date:
        dayP = product['date'][8:10]
        monthP = product['date'][5:7]
        yearP = product['date'][0:4]
        fecha = yearP + "/" + monthP + "/" + dayP

        yearS = start_date[0:4]
        monthS = start_date[5:7]
        dayS = start_date[8:10]

        fechaS = yearS + "/" + monthS + "/" + dayS

        yearE = end_date[0:4]
        monthE = end_date[5:7]
        dayE = end_date[8:10]

        fechaE = yearE + "/" + monthE + "/" + dayE

        fecha = time.strptime(fecha, "%Y/%m/%d")
        fechaS = time.strptime(fechaS, "%Y/%m/%d")
        fechaE = time.strptime(fechaE, "%Y/%m/%d")

        hora = product['date'][11:14]

        if fecha > fechaS:
            if(fecha < fechaE):
                if(hora >= valueS[0:2]):
                    if(hora <= valueE[0:2]):
                        data.append(product)

    return data


@app.callback(dash.dependencies.Output('table_placeholder', 'children'), 
              dash.dependencies.Input('store-data', 'data'))
def update_table(data):
    df = pd.DataFrame(data)

    myTable = dash_table.DataTable(
        columns = [{"name": i, "id": i} for i in df.columns],
        data = df.to_dict('records'),
        sort_action='native'
    )
    return myTable

@app.callback(dash.dependencies.Output('total_price', 'children'), 
              dash.dependencies.Input('store-data', 'data'))
def update_table(data):
    total_price = 0 
    for product in data:
        total_price += product['price']
    return html.H5(f"Total Price: {total_price}")
