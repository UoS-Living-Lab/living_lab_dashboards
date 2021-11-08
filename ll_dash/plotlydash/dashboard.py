"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
from dash import dash_table
from dash import html
from dash import dcc
import plotly.graph_objects as go
from .data import create_dataframe, get_ttn_data, get_sel_data
from .layout import html_layout


def init_dashboard(server):
	"""Create a Plotly Dash dashboard."""
	dash_app = dash.Dash(
		server=server,
		routes_pathname_prefix='/dashapp/',
		external_stylesheets=[
			'/static/dist/css/styles.css',
			'https://fonts.googleapis.com/css?family=Lato'
		]
	)

	# Load DataFrame
	df = create_dataframe()

	# Custom HTML layout
	dash_app.index_string = html_layout


	def update_ttn_scatter():
		df = get_ttn_data("Temperature")
		X = df['received_at']
		Y = df['sensor_value']

		data = go.Scatter(
				x=list(X),
				y=list(Y),
				name='Temperature',
				mode= 'lines+markers'
				)
		layout = go.Layout(
			title = 'Temperature'
			)

		return {'data': [data],'layout' : [layout]}

	def update_sel_scatter():
		df = get_sel_data("Moisture Sensor 1")
		X = df['lastUpdate']
		Y = df['readingValue']

		data = go.Scatter(
				x=list(X),
				y=list(Y),
				name='Moisture Sensor 1',
				mode= 'lines+markers'
				)
		layout = go.Layout(
			title = 'Moisture Sensor 1'
			)

		return {'data': [data],'layout' : [layout]}


	# Create Layout
	dash_app.layout = html.Div(
		children=[dcc.Graph(
			id='histogram-graph',
			figure={
				'data': [{
					'x': df['complaint_type'],
					'text': df['complaint_type'],
					'customdata': df['key'],
					'name': '311 Calls by region.',
					'type': 'histogram'
				}],
				'layout': {
					'title': 'NYC 311 Calls category.',
					'height': 500,
					'padding': 150
				}
			}),
			dcc.Graph(id='ttn', figure = update_ttn_scatter()),
			dcc.Graph(id='sel', figure = update_sel_scatter()),
			create_data_table(df)
		],
		id='dash-container'
	)
	return dash_app.server


def create_data_table(df):
	"""Create Dash datatable from Pandas DataFrame."""
	table = dash_table.DataTable(
		id='database-table',
		columns=[{"name": i, "id": i} for i in df.columns],
		data=df.to_dict('records'),
		sort_action="native",
		sort_mode='native',
		page_size=300
	)
	return table