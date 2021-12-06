"""Instantiate a Dash app."""
from datetime import date, timedelta
import numpy as np
import pandas as pd
import dash
from dash import dash_table
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from .data import create_dataframe, get_ttn_data, get_sel_data, get_csv_data
from .layout import html_layout


def init_dashboard(server):
	dash_app = dash.Dash(
		server=server,
		routes_pathname_prefix='/dashapp/',
		external_stylesheets=[
			'/static/dist/css/styles.css',
			'https://fonts.googleapis.com/css?family=Lato'
		],
		prevent_initial_callbacks=True
	)

	# Load DataFrame
	df = create_dataframe()


	#TESTING
	data = np.column_stack((np.arange(10), np.arange(10) * 2))
	df = pd.DataFrame(columns=["a column", "another column"], data=data)
	
	today = date.today().strftime('%Y-%m-%d')
	
	last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
	start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
	

	#TESTING


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
									title='TTN: ' + sensor,)}

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
									title= unit + ': ' + sensor,)}


	# Create Layout
	dash_app.layout = html.Div(
		children=[
			html.Div(
				children=[
					html.Div(),
					dcc.DatePickerRange(
						id = 'my-date-picker-range',
						display_format = 'Y-M-D',
						min_date_allowed = today,
						max_date_allowed = today,
						initial_visible_month = start_day_of_prev_month,
						start_date = start_day_of_prev_month,
						end_date = today
					),
					html.Button("Download CSV", id="btn"), dcc.Download(id="download"),
					html.Div()
					], className='DL-BTN'
			),
			html.Div(
				children=[
					dcc.Graph(id='ttn-temp', figure = ttn_scatter("Temperature")),
				],
				className='TTN'
			),
			html.Div(
				children=[
					dcc.Graph(id='sel-cp2-ms1', figure = sel_scatter("Moisture Sensor 1", "Control Panel 2 PH1")),
					dcc.Graph(id='sel-cp2-ms2', figure = sel_scatter("Moisture Sensor 2", "Control Panel 2 PH1")),
					dcc.Graph(id='sel-cp2-l1', figure = sel_scatter("Level 1", "Control Panel 2 PH1")),
					dcc.Graph(id='sel-lw-graw', figure = sel_scatter("Grey Wall", "Live Wall PH2")),
					dcc.Graph(id='sel-lw-grew', figure = sel_scatter("Green Wall", "Live Wall PH2")),
					dcc.Graph(id='sel-lw-redw', figure = sel_scatter("Red Wall", "Live Wall PH2")),
					dcc.Graph(id='sel-lw-bluw', figure = sel_scatter("Blue Wall", "Live Wall PH2")),
					dcc.Graph(id='sel-climbers', figure = sel_scatter("Climbers", "8C:5C:E4:E0:79:6D")),
					dcc.Graph(id='sel-ignigtion-mix', figure = sel_scatter("Ignition-mix ", "8C:EF:8C:0D:2F:8F")),
					dcc.Graph(id='sel-level-cp1', figure = sel_scatter("Level ", "Control Panel 1 PH1")),
					dcc.Graph(id='sel-live-wall', figure = sel_scatter("Live Wall", "Control Panel 5 PH1")),
					dcc.Graph(id='sel-meadow', figure = sel_scatter("Meadow ", "8C:5C:E4:E0:79:6D")),
					dcc.Graph(id='sel-cp3-ms1', figure = sel_scatter("Moisture Sensor 1", "Control Panel 3 PH1")),
					dcc.Graph(id='sel-cp4-ms1', figure = sel_scatter("Moisture Sensor 1", "Control Panel 4 PH1")),
					dcc.Graph(id='sel-cp1-ms2', figure = sel_scatter("Moisture Sensor 2", "Control Panel 1 PH1")),
					dcc.Graph(id='sel-cp1-ms3', figure = sel_scatter("Moisture Sensor 3", "Control Panel 1 PH1")),
					dcc.Graph(id='sel-planters', figure = sel_scatter("Planters ", "8C:5C:E4:E0:79:6D")),
					dcc.Graph(id='sel-s001-level', figure = sel_scatter("S001 Level", "S24 Main Panel PH2")),
					dcc.Graph(id='sel-s24-level;', figure = sel_scatter("S24 Level", "S24 Main Panel PH2")),
					dcc.Graph(id='sel-sedum;', figure = sel_scatter("Sedum", "8C:EF:8C:0D:2F:8F")),
					dcc.Graph(id='sel-sunken-planter;', figure = sel_scatter("Sunken Planter Level", "Control Panel 5 PH1")),
					dcc.Graph(id='sel-tank-level;', figure = sel_scatter("Tank level ", "S24 Main Panel PH2")),
					dcc.Graph(id='sel-tree;', figure = sel_scatter("Tree", "8C:EF:8C:0D:2F:8F")),
					dcc.Graph(id='sel-wonderwall;', figure = sel_scatter("WonderWall", "8C:5C:E4:E0:79:6D")),
				],
				className='SEL'
			),
		],
		className='dash-container'
	)
	@dash_app.callback(
		Output("download", "data"), 
		[
			Input("btn", "n_clicks"),
			Input('my-date-picker-range', 'start_date'),
			Input('my-date-picker-range', 'end_date')
		],)
	def generate_csv(n_nlicks, start_date, end_date):
		data = get_csv_data(start_date, end_date)
		return dcc.send_data_frame(data.to_csv, filename="living_lab_data.csv")

	return dash_app.server
