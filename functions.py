
from globals import DATABASE_URI
from globals import DATABASE_DEFAULT_USERNAME,DATABASE_DEFAULT_PASSWORD
from py2neo import Graph


graph_driver = lambda username,password: Graph(uri=DATABASE_URI,auth=(username,password))

default_driver = graph_driver(DATABASE_DEFAULT_USERNAME, DATABASE_DEFAULT_PASSWORD)