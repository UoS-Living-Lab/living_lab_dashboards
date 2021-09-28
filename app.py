import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots



irrigation_flow = []
inlet_flow = []
irrigation_datetime = []

moisture_sensor = []
moisture_sensor2 = []
moisture_datetime = []

import csv
with open("./data/flow.csv", newline='') as csvfile:
	flow = csv.DictReader(csvfile)
	for row in flow:
		irrigation_flow.append(float(row['Irrigation Flow'].replace(" ", "").replace('"', '')))
		inlet_flow.append(float(row[' "Inlet Flow"'].replace(" ", "").replace('"', '')))
		irrigation_datetime.append(row['  Date/Time'])

with open("./data/moisture_level.csv", newline='') as csvfile:
	moisture = csv.DictReader(csvfile)
	for row in moisture:
		moisture_sensor.append(int(row[' Moisture Sensor 3( % )']))
		moisture_sensor2.append(int(row[' Moisture Sensor 2( % )']))
		moisture_datetime.append(row['Date'])


moisture_flow = go.Figure()
moisture_flow = make_subplots(specs=[[{"secondary_y": True}]])
moisture_flow.add_trace(go.Scatter(x = irrigation_datetime, y=irrigation_flow, name= 'Irrigation Flow'), secondary_y=False,)
moisture_flow.add_trace(go.Scatter(x = irrigation_datetime, y=inlet_flow, name= 'Inlet Flow'), secondary_y=False,)
moisture_flow.add_trace(go.Scatter(x=moisture_datetime, y=moisture_sensor, name= 'Moisture Sensor'), secondary_y=True,)
moisture_flow.add_trace(go.Scatter(x=moisture_datetime, y=moisture_sensor2, name= 'Moisture Sensor 2'), secondary_y=True,)
moisture_flow.update_layout(title="Soil Moistuer/Water Flow", xaxis_title="Datetime")


moisture_flow.update_yaxes(
	title_text="Irrigation Flow", 
	secondary_y=False
)
moisture_flow.update_yaxes(
	title_text="Moisture Level", 
	secondary_y=True
)


app = dash.Dash(__name__)

app.layout = html.Div([
	dcc.Graph(
				id ="m_f",
				figure = moisture_flow
			)
])

if __name__ == "__main__":
	app.run_server(debug=True, host='0.0.0.0', port='80')