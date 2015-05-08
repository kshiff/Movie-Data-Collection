'''
Karl Shiffler (shiffler@bu.edu)

Script downloads Rotten Tomatoes pages for movies in the Netflix data page.
Must be run in a directory with movie_titles.txt and folders /data/ and /ratingdata/

NOTE:
This script is made obsolete by tomatorating.py

'''
from lxml import etree #import iterparse
import numpy as np
import cPickle as pickle
from imdb import IMDb 
import csv
import requests
import os
import time
import json

key = '?apikey=3a8krz5sauwa37v534bkrzu8'


base = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'

format = '[your_api_key]&q=Toy+Story+3&page_limit=1'

datadir = './data/'
ratingdir = './ratingdata/'

with open("movie_titles.txt", 'rb') as inTitles:
	titleReader = csv.reader(inTitles)
	for i, titleInfo in enumerate(titleReader):
		# if i > 2668:

		response = requests.get(base + key + "&q=" + title)
		j = response.text.encode('utf-8')

		with open(os.path.join(datadir, title + '-json.json'), "w") as h:
			h.write(j)

		time.sleep(.2)

		d = json.loads(j)
		for x in range(len(d['movies'])):
			# print json.dumps(d['movies'][x], indent=4)#d['movies'][0]['year'] #json.dumps(d, indent=4)
			# print d['movies'][x]['title'], d['movies'][x]['year']

			link = d['movies'][x]['links']['reviews']
			if d['movies'][x]['year'] != '' and year != "NULL":
				if int(year) == int(d['movies'][x]['year']):
					
					response = requests.get(link + key)
					n = response.text.encode('utf-8')

					with open(os.path.join(ratingdir, title + '-json.json'), "w") as h:
						h.write(n)
					time.sleep(.2)



