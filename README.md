# plotly-database-tutorial

https://www.kaggle.com/rtatman/lego-database#sets.csv

We have data. How can we meaningfully display it? A graph is the most useful and easiest way to display data, but building one by hand from information from a csv or database can be challenging. However, by using ```python``` and ```plotly```, a chart making library, we can do this in just a few lines of code. 

For this example, we can use a free online data set of all the Lego sets that have been released (which can be downloaded as a .csv file). We will learn how to pull data from a csv or database into a ```pandas``` dataframe in ```python```, then display it using ```plotly```. All this code can be easily written in and run from a jupyter notebook.

The first step is to check out our data and how it is collected. Viewing the data, we see that we have five columns, the set id, name, year, theme, and number of parts. It's ordered by the id string.

For this example, we are going to try to output a chart that displays the number of sets that have been released every year since 2000. 

After a little bit of research, ```plotly``` offers a free version of itself called ```plotly offline```. In a jupyter notebook, we begin by importing this, and ```pandas``` so we can pull the database info into a dataframe.
```
	import pandas as pd

	import plotly.offline as pl
	import plotly.graph_objs as go
```	

From the plotly website, since we are using notebook, we just have to add one more line.
```
	pl.init_notebook_mode()
```
Now comes the tricky step: pulling data into a ```pandas``` dataframe. Right now it’s in a csv file, but what if it was in a sqlite database? Or another online database?

#### Method 1: Pulling directly from a .csv file

Our data is already in a .csv file, so we can pull it directly into a ```pandas``` dataframe in two lines.
```
  read_df = pd.read_csv("sets.csv") 
  df = read_df.query("year>=2000", inplace = True)
```

#### Method 2: Pulling from a local sqlite database
For this method, we are first going to set up a sqlite database from our .csv, then query that database. First we need to import ```sqlite3``` and csv, and open a connection to our database file (which creates it if it doesn’t exist). Finally we set up a cursor to execute our SQL statements. 

```
  import sqlite3, csv
  conn = sqlite3.connect("sets.db")
  cur = conn.cursor()
```
The first step is to make sure we are not making a duplicate table. An error will be thrown if you try to create two tables with the same name, so we must drop it if it already exists. 
```
  cur.execute("DROP TABLE if exists SETS")
```
Next we set up our table with the same schema and column names as the csv file. 
```
  cur.execute("CREATE TABLE SETS (set_num STR, name STR, year STR, theme_id INT, num_parts INT, PRIMARY KEY(set_num))") 
```
Finally we need to read the values from the csv file into the table. ```open()``` is a python method that takes the name of the file, action (```r``` is for ‘read’) and we need to specify the encoding to make sure all the symbols are understood. Checking our .csv file, all the information is separated by commas, so we set our delimiter to be a comma and read it into an ordered dictionary. Then we convert each set in the dictionary to a list. 

```
with open('sets.csv','r', encoding = 'utf8') as sets_table:
    dr = csv.DictReader(sets_table, delimiter=',') # comma is default delimiter
    to_db = [(i['set_num'], i['name'], i['year'], i['theme_id'], i['num_parts']) for i in dr]
```
Finally, we form our SQL statement to insert all the data row by row into the database, passing to_db as a parameter to replace the placeholder question marks in the statement. ```executemany()``` will keep passing the rows in, and then we can commit these changes. 
```
cur.executemany("INSERT INTO sets VALUES (?,?,?,?,?);", to_db)
conn.commit()
```
Now that we’ve set up access to our database, we have to actually come up with the query. If you already know SQL this is completely up to you what information you'd like to pull, but for simplicity's sake, our query has the condition ```request year>=2000```. We then store this query in a string.

```
  query = """
    select * 
    from sets 
    where year>=2000
	"""
```
Now our query pulls all the outgoing requests. We will put this data into a pandas dataframe, and then close the connection so we don’t lock the database when we are not using it. 
```
  df= pd.read_sql_query(query, conn)
  cur.close()
  conn.close()
```
	
#### Method 2.5: Pulling from an online database you have access to
This method assumes you have access to an online database. Since our data is not available in this manner, it won’t work for this particular set, but here is the code that would be needed: 

From sqlalchemy weimport something called create_engine to deal with connecting to our database. We just need the ip, port, database name, username and password to connect now.

```
  from sqlalchemy import create_engine
  mysql_engine = create_engine('mysql+pymysql://<username>:<password>@<ip>:<port>/<database_name>?charset=utf8', encoding = 'utf-8',  echo=False)

```
Our query and pulling it into a dataframe is similar to above.

```
  query = """
    	select * 
    	from <database_name>
    	where <condition>
	"""
	df = pd.read_sql(query, mysql_engine)

```

We can display the dataframe to observe its structure, but it's essentially the same as the database. From here, we need to decide on what type of chart we want and what axis. We want to see the number of sets per year, so ```year``` should be our x axis and ```count``` should be our y axis.

The easiest way to set up for plotly is to make a dataframe with the exact data you're going to put in. We are going to make a new dataframe that has a column of all the possible years (so 2000 to this year) and another column for the counts. To find those counts, we are going to use the value_counts() function that counts the number of times each year appears. However, we have to be careful, since the function will automatically reorder that column, so we have to use ```reset_index()``` to make sure they correspond to the right year. Finally, to save us some trouble, we will rename our columns.
```
final_df=df['year'].value_counts().reset_index().rename(columns={"index":"year", "year":"count"})
```
Just in case your year values are all in a crazy order, you can easily sort them. Just remember to use inplace = True so your dataframe will change itself if you're not assigning it to another variable.
```
  final_df.sort_values(by='year', ascending=True, inplace=True)
```
	or
```
  final_df_sorted = final_df.sort_values(by='year', ascending=True)
```
Now that our dataframe is down to just what we need, we can start with the plotly! Our data is probably best represented in a bar graph. Inside our bar graph object, we will first set the axes.
```
	trace1 = go.Bar(
		x=final_df['year'],
		y=final_df['count'],
	
	)
```

Now this is the baseline for our graph, but we want it to be a bit nicer to look at. Plotly's website has a lot of good examples of how exactly you can mess with the look of your charts.
```
	trace1 = go.Bar(
		x=final_df['year'],
		y=final_df['count'],
		marker=dict(
			color='rgb(255,129,10)',
			line=dict(
				color='rgb(255,129,0)',
				width=1.5),
			),
    	opacity=0.75
	)
```
This only will change the bars in the chart, to change the axis and give the chart a title, we need a layout object.
```
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
			range=[0,final_df['counts'].max()+100],
			showticklabels=True
		)
	)
```
Finally, we will put it all together and output our chart. Remember that go.Figure takes an array of chart objects, so although we only have one data set, we need to put it in an array.
```
	fig = go.Figure(data = [trace1], layout=layout)
	pl.iplot(fig, filename="lego.html")
```

Now you know how easy it is to represent your data in a plotly graph with just a few lines. Enjoy!

