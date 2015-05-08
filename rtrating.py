'''
Karl Shiffler (shiffler@bu.edu)

Script iterates through Rotten Tomatoes ratings downloads and parses information into csv files.
Must be run in the same directory as the movie_titles.txt file and the folder /ratingdir/ containing the JSON files for the movies' reviews.

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
import os.path

key = '?apikey=3a8krz5sauwa37v534bkrzu8'

review_type = '&review_type=all'

base = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'

pg_limit = "&page_limit=50"

ratingdir = "./newratingdata/"
datadir = './newdata/'

def formatRow(review):
	critic, date, fresh, pub, original_score = (None, None, None, None, None)
	if review['critic'] != "":
		critic = review['critic']
	if review['date'] != "":
		date = review['date']
	if review['freshness'] == 'fresh':
		fresh = 1
	elif review['freshness'] == 'rotten':
		fresh = -1
	else:
		fresh = 0
	if review['publication'] != "":
		pub = review['publication']
	if 'original_score' in review:
		original_score = review['original_score']

	return (critic,date,fresh,pub,original_score)



with open("movie_titles.txt", 'rb') as inTitles:
	titleReader = csv.reader(inTitles)
	with open("RTratings.csv", 'wb') as rOut:
		sw = csv.writer(rOut)
		sw.writerow(("title","year","critic", "date", "freshness", "publication", "original_score"))
		for i, titleInfo in enumerate(titleReader):
			# if i > 14628: # number of the movie you want to start on; added so I could process movies in chunks
			print i 
			origTitle = titleInfo[2]
			title = titleInfo[2].replace("/ ", "").replace(" /", "").replace("/", "").replace(" ","+").replace("?","")
			year = titleInfo[1]
			data = (origTitle, year)
			# we have the movie file
			if os.path.isfile(ratingdir + title + '1' + "-json.json"):
				with open(ratingdir + title + '1' + "-json.json") as mov:
					
					m = json.load(mov)

					# reviews on multiple pages
					if m['total'] != len(m['reviews']):
						pgs = m['total'] / 50 + (m['total'] % 50 > 0)
						
						for page in range(1,pgs+1):
							
							with open(os.path.join(ratingdir, title + str(page) + '-json.json')) as h:
								rat = json.load(h)
								for rev in rat['reviews']:
									sw.writerow(data + formatRow(rev))


					else: # reviews on one page
						for rev in m['reviews']:
							sw.writerow(data + formatRow(rev))





			# we don't have the movie file
			# else:
			# 	f = 1 
			# 	tot = 100
			# 	while not os.path.isfile(ratingdir + title + "-json.json"):
			# 		if (f-1 * 50) > tot:
			# 			break

			# 		response = requests.get(base + key + pg_limit + "&q=" + title + "&page=" + str(i))
			# 		j = response.text.encode('utf-8')

			# 		with open(os.path.join(datadir, title + '-json.json'), "w") as h:
			# 			h.write(j)

			# 		time.sleep(.2)
			# 		d = json.loads(j)
			# 		tot = d['total']
					
			# 		for x in range(len(d['movies'])):

			# 			link = d['movies'][x]['links']['reviews']
			# 			if d['movies'][x]['year'] != '' and year != "NULL":
			# 				if int(year) == int(d['movies'][x]['year']):
			# 					response = requests.get(link + key + pg_limit)
			# 					n = response.text.encode('utf-8')

			# 					with open(os.path.join(ratingdir, title + '-json.json'), "w") as h:
			# 						h.write(n)
			# 					time.sleep(.2)
			# 		f = f + 1
			# 	if os.path.isfile(ratingdir + title + "-json.json"):
			# 		with open(ratingdir + title + "-json.json") as mov:
			# 			m = json.load(mov)

			# 			# we don't have all reviews
			# 			if m['total'] != len(m['reviews']):
			# 				pgs = m['total'] / 50 + (m['total'] % 50 > 0)
							
			# 				for page in range(1,pgs+1):
			# 					response = requests.get(link + key + pg_limit + "&page=" + page)
			# 					n = response.text.encode('utf-8')

			# 					# this may create duplicates of first 20 reviews
			# 					with open(os.path.join(ratingdir, title + str(page) + '-json.json'), "w") as h:
			# 						h.write(n)

			# 					rat = json.load(n)
			# 					for rev in rat['reviews']:
			# 						sw.writerow(title, year, formatRow(rev))


			# 			else: # we have all reviews
			# 				for rev in m['reviews']:
			# 					sw.writerow(title, year, formatRow(rev))



# print len(num)
# print max(num)


# for tit in num:
	# with open(datadir + tit + '-json.json') as extra:


# pickle.dump(num, open("extraRevs.pckl", "wb"))