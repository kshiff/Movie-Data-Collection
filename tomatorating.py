'''
Karl Shiffler (shiffler@bu.edu)

Script iterates through Netflix data and downloads Rotten Tomatoes pages and the ratings pages.
Must be run in a directory with movie_titles.txt and folders /newdata/ and /newratingdata/

'''
from lxml import etree #import iterparse
import numpy as np
import cPickle as pickle
from imdb import IMDb 
import csv
import requests
import os
import time
import bs4 as BeautifulSoup
import json

key = '?apikey=3a8krz5sauwa37v534bkrzu8'

review_type = '&review_type=all'

base = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'

pg_limit = "&page_limit=50"

datadir = './newdata/'
ratingdir = './newratingdata/'

with open("movie_titles.txt", 'rb') as inTitles:
	titleReader = csv.reader(inTitles)
	for i, titleInfo in enumerate(titleReader):
		if i > 15637: # number of the movie you want to start on; added so I could process movies in chunks
			title = titleInfo[2].replace("/ ", "").replace(" /", "").replace("/", "").replace(" ","+").replace("?","")
			year = titleInfo[1]
			



			# print title, year

			# find all movies matching the query
			response = requests.get(base + key + pg_limit + "&q=" + title)
			j = response.text.encode('utf-8')

			with open(os.path.join(datadir, title + '1' + '-json.json'), "w") as h:
				h.write(j)

			time.sleep(.2)
			d = json.loads(j)

			pgs = d['total'] / 50 + (d['total'] % 50 > 0)

			if pgs > 1:
				for page in range(2,pgs+1):
					response = requests.get(base + key + pg_limit + "&q=" + title + "&page=" + str(page))
					j = response.text.encode('utf-8', 'ignore')

					with open(os.path.join(datadir, title + str(page) + '-json.json'), "w") as h:
						h.write(j)

					time.sleep(.2)
					d = json.loads(j)

			#search through movies
			for page in range(1,pgs+1):
				print "movie " + str(page)
				with open(os.path.join(datadir, title + str(page) + '-json.json')) as h:
					d = json.load(h)

					for x in range(len(d['movies'])):

						link = d['movies'][x]['links']['reviews']
						if d['movies'][x]['year'] != '' and year != "NULL":
							if int(year) == int(d['movies'][x]['year']):
								
								response = requests.get(link + key + pg_limit + review_type)
								n = response.text.encode('utf-8', 'ignore')

								js = json.loads(n)
								rPgs = js['total'] / 50 + (js['total'] % 50 > 0)

								with open(os.path.join(ratingdir, title + '1' + '-json.json'), "w") as h:
									h.write(n)
								time.sleep(.2)
								if rPgs > 1:
									for pg in range(2,rPgs+1):
										print "review " + str(pg)
										res = requests.get(link + key + pg_limit + review_type + "&page=" + str(pg))
										r = res.text.encode('utf-8', 'ignore')
										with open(os.path.join(ratingdir, title + str(pg) + '-json.json'), "w") as h:
											h.write(r)
										time.sleep(.2)

								break
					else:
						continue
					break

			print "---------------------" + str(i)