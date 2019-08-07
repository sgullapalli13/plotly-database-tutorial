from flask import Flask, render_template

import pandas as pd
from datetime import datetime

import plotly as plotly
import plotly.offline as pl
import plotly.graph_objs as go
#you only need to import these based on how you are accessing your data
from sqlalchemy import create_engine
import csv
import sqlite3 as sq
import json


app= Flask(__name__)

@app.route("/")
def index():
	data = pd.read_csv("sets.csv")
	data.query('year>=2000',inplace=True)

	final_df=data['year'].value_counts().reset_index().rename(columns={"index":"year", "year":"counts"})
	final_df_ordered= final_df.sort_values(by='year', ascending=True)

	traces = []
	traces.append(go.Bar(
		x=final_df_ordered['year'],
		y=final_df_ordered['counts'],
		marker=dict(
			color='rgb(255,129,10)',
			line=dict(
				color='rgb(255,129,0)',
				width=1.5),
			),
		opacity=0.75,
	))

	layout= go.Layout(
		title = go.layout.Title(
			text='Lego sets per year',
			font = dict(
				family = 'Trebuchet',
				size = 18,
				color = 'rgb(255,129,10)'
			)
		),
		yaxis=dict(
			range=[0,final_df_ordered['counts'].max()+100],
			showticklabels=True
		)
	)

	fig = go.Figure(data = traces, layout=layout)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return render_template('index.html', graph_json = graphJSON)


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8080)
