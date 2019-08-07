# plotly-database-tutorial: Part 2

Note: This is a continuation of a tutorial. For Part 1 on learning how to pull databases into a pandas dataframe and displaying with plotly, see plotly-database-tutorial/Part 1. 

We have figured out how to display our database information in a plotly graph, but now we want to display our information on the web. Using ```Flask```, we can build a lightweight web app that will display our data. Following the previous tutorial, all the code that deals with accessing the databases and plotly is in a jupyter notebook, so we can easily transfer that.

First, we make a folder in our file system, and within that make two files: one called app.py, and another called requirements.txt. Then make a subfolder called templates, and within that an html file called index.html. In your main folder add your downloaded sets.csv.

In requirements.txt, add the following:
```
Flask
SQLAlchemy
Flask-SQLAlchemy
Plotly
Pandas
```
If you haven’t downloaded all of these yet to your computer, open a command prompt and type pip install -r requirements.txt, or download them individually. (Note: it’s important to keep track of where you install these and what versions they are. Another program you write may need a different version, so it’s important to avoid conflicts/deprecated code.) In your requirements file, you can update the version numbers. For example:
```
…
plotly==3.6
Flask>=0.12
```
I especially recommend this for plotly, as it gets updated pretty often so parts of their syntax are often deprecated. 

Next, in app.py, add all imports from your jupyter notebook code, along with 
```
from flask import Flask, render_template

import pandas as pd
from datetime import datetime

import plotly as plotly
import plotly.offline as pl
import plotly.graph_objs as go

#you only need to import these based on how you are accessing your data
from sqlalchemy import create_engine
import csv, sqlite3
```
Next, we are going to initialize our app, and add a function that runs when someone visits our page. 
```
app= Flask(__name__)

@app.route("/")
def index():
	return
```
`app.route("/")` is referring to the path in a url. For now, we can keep it as the base url.
Inside our ```index()``` function, we can essentially copy and paste in our jupyter notebook code. For this I'm using Method 1 from the previous tutorial.
```
def index():
	data = pd.read_csv("sets.csv")
 	data.query('year>=2000',inplace=True)
…

fig = go.Figure(data = traces, layout=layout)
#pl.iplot(fig, filename="lego.html")
return
```
The last lines of the code need to be changed, because instead of producing an inline plot, we need to convert the plot to JSON and pass it to the front end. First, we have to make a place for the plot to go in the front end. Open index.html and make a div for the plot to be placed in, giving it a descriptive id. 
```
<!DOCTYPE html>
<html>
<head lang=”en”>
	<meta charset=”UTF=8”>
</head>
<body>
	Hello World!
	<div id= “graphdiv”> </div>
</body>
<script>
</script>
</html>
```

Next, in our ```index()``` function, we change our iplot line to instead turn the chart code into JSON using plotly’s built-in encoder. 

```
fig = go.Figure(data = traces, layout=layout)
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
```
Flask has a ```render_template()``` function that takes an html file and any number of variables that it will pass to the front end. Flask will check in a templates folder for your html, so we can just write:
```
fig = go.Figure(data = traces, layout=layout)
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
return render_template('index.html', graph_json = graphJSON)
```
This is passing a variable called  ‘graph_json’ to our front end. We go back into index.html to turn it into a graph. First, we add plotly’s javascript version in a script tag.
```
<html>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
….
```

Flask comes with jinja2, an easy way of passing variables writing script in the html. Down in the script tags, we make a javascript variable and assign it to the passed graph_json. Then we plot the graph, passing the plotly function the id of the div we want it in, the JSON, and another argument that tells the graph to be responsive and resize to fit the window.
```
…
</body>
<script>
	var graph = {{ graph_json | safe }};
	Plotly.plot('graphdiv', graph, {responsive: true});
</script>
</html>
```

Flask defaults to running our app on port 5000, but to specify another port, in our app.py file we can add:
```
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8080)
```

In a terminal we can run ```python app.py```, and then go to a browser to visit localhost:8080 to view our work.

