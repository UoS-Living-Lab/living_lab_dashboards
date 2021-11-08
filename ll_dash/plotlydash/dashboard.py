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


	def ttn_scatter(sensor):
		df = get_ttn_data(sensor)
		X = df['received_at']
		Y = df['sensor_value']

		data = go.Scatter(
				x=list(X),
				y=list(Y),
				name='Temperature',
				mode= 'lines+markers'
				)

		return {'data': [data],'layout' : go.Layout(
									title='TTN :' + sensor,)}

	def sel_scatter(sensor, unit):
		df = get_sel_data(sensor, unit)
		X = df['lastUpdate']
		Y = df['readingValue']

		data = go.Scatter(
				x=list(X),
				y=list(Y),
				name=sensor,
				mode= 'lines+markers'
				)
		layout = go.Layout(
			title = sensor
			)

		return {'data': [data],'layout' : go.Layout(
									title='SEL :' + sensor,)}


	# Create Layout
	dash_app.layout = html.Div(
		children=[
			dcc.Graph(id='ttn-temp', figure = ttn_scatter("Temperature")),
			dcc.Graph(id='sel-cp2-ms1', figure = sel_scatter("Moisture Sensor 1", "Control Panel 2 PH1")),
			dcc.Graph(id='sel-cp2-ms2', figure = sel_scatter("Moisture Sensor 2", "Control Panel 2 PH1")),
			dcc.Graph(id='sel-cp2-l1', figure = sel_scatter("Level 1", "Control Panel 2 PH1")),
			dcc.Graph(id='sel-lw-graw', figure = sel_scatter("Grey Wall", "Live Wall PH2")),
			dcc.Graph(id='sel-lw-grew', figure = sel_scatter("Green Wall", "Live Wall PH2")),
			dcc.Graph(id='sel-lw-redw', figure = sel_scatter("Red Wall", "Live Wall PH2")),
			dcc.Graph(id='sel-lw-bluw', figure = sel_scatter("Blue Wall", "Live Wall PH2")),
		],
		id='dash-container'
	)
	return dash_app.server

