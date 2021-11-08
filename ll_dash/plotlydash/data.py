"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd

import pyodbc
from decouple import config


# Batabase access credentials
DB_URL = config('AZURE_DB_SERVER')
DB_BATABASE = config('AZURE_DB_DATABASE')
DB_USR = config('AZURE_DB_USR')
DB_PWD = config('AZURE_DB_PWD')


def create_dataframe():
	"""Create Pandas DataFrame from local CSV."""
	df = pd.read_csv("data/311-calls.csv", parse_dates=["created"])
	df["created"] = df["created"].dt.date
	df.drop(columns=["incident_zip"], inplace=True)
	num_complaints = df["complaint_type"].value_counts()
	to_remove = num_complaints[num_complaints <= 30].index
	df.replace(to_remove, np.nan, inplace=True)
	return df


def connect_sql_server():
	# Formatted connection string for the SQL DB.
	SQL_CONN_STR = "DSN={0};Database={1};UID={2};PWD={3};".format(DB_URL, DB_BATABASE, DB_USR, DB_PWD)
	
	conn = pyodbc.connect(SQL_CONN_STR)
	return conn


def get_ttn_data(sensor_name):
	data = []

	conn = connect_sql_server()
	cursor = conn.cursor()
	SQL = '''
		SELECT s.[sensor_name], r.[sensor_value], dt.[received_at]
		FROM [dbo].[TTN_READINGS] as r
		JOIN [dbo].[TTN_SENSORS] as s
			ON r.[sensor_guid] = s.[sensor_guid]
		JOIN [dbo].[TTN_DATETIMES] as dt
			ON r.[uplink_guid] = dt.[uplink_guid]
		WHERE s.[sensor_name] = ?
		ORDER BY dt.[received_at] DESC
	'''

	params = str(sensor_name)
	cursor.execute(SQL, params)
	rows = cursor.fetchall()
	conn.close()

	for row in rows:
		data.append(list(row))
		labels = ['sensor_name','sensor_value', 'received_at']
		df = pd.DataFrame.from_records(data, columns=labels)

	return df


def get_sel_data(sensor_name):
	data = []

	conn = connect_sql_server()
	cursor = conn.cursor()
	SQL = '''
		SELECT s.[sensorName], u.[unitName], mu.[mUnitName], r.[readingValue], up.[lastUpdate]
		FROM [dbo].[SEL_READINGS] as r
		JOIN [dbo].[SEL_SENSORS] as s
			ON (r.[sensorGUID] = s.[sensorGUID])
		JOIN [dbo].[SEL_UNITS] as u
			ON r.[unitGUID] = u.[unitGUID]
		JOIN [dbo].[SEL_MEASURE_UNITS] as mu
			ON r.[mUnitGUID] = mu.[mUnitGUID]
		JOIN [dbo].[SEL_UPDATES] as up
			ON r.[readingGUID] = up.[readingGUID]
		WHERE s.[sensorName] = ?
		ORDER BY up.[lastUpdate] DESC
	'''

	params = str(sensor_name)
	cursor.execute(SQL, params)
	rows = cursor.fetchall()
	conn.close()

	for row in rows:
		data.append(list(row))
		labels = ['sensorName','unitName', 'mUnitName', 'readingValue', 'lastUpdate']
		df = pd.DataFrame.from_records(data, columns=labels)
	
	return df