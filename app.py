from flask import Flask, render_template, redirect
import pandas as pd
from bokeh.plotting import figure
import ujson as json
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.embed import components
import os
import gunicorn


app = Flask(__name__)

@app.route('/')
def main():
	return redirect('/test')

@app.route('/test')
def index():
	print "index started"
	pathdata=os.path.join(os.getcwd(),"static","data","goog.json")
	with open(pathdata) as raw_f:
		raw_data = raw_f.read()
	json_data = json.loads(raw_data)
	print "data loaded"
	df = pd.DataFrame(json_data['data'], columns=json_data['column_names'])
	df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
	print "dataframe created"
	plot = figure(title="Title", x_axis_label="date", x_axis_type="datetime")
	plot.line(df["Open"].index[0:], df["Open"][0:])
	print "chart created"
	script1,div1 = components(plot) #components is creating java code for html, script is the script, div is the tag
	html=render_template('pages/index.html',script1=script1,div1=div1)
	print "index ended"
	return html

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=33507)
