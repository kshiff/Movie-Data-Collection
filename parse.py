'''
Written by Karl Shiffler (shiffler@bu.edu)

Parses Netflix XML file from Netflix data challenge and produces CSV files containing:
title, year, rating, date DVD is available from, date DVD is available until, date instant is available from, 
date instant is available until, runtime (seconds), language, audio

All in a format easily imported into an SQL database.

Must be run in the same directory as movies_full.xml
'''
from lxml import etree #import iterparse
import numpy as np
import cPickle as pickle
from imdb import IMDb 
import csv

# ia = IMDb('sql', uri='mysql://root@localhost:3306/imdb')

i=0

def correctID(movies, year):
	'''
	Returns the correct ID given a list of movie objects and the year of the desired move.

	Parameters:
	movies:	list of movie objects from IMDb.py 
	year:	year of desired movie

	Returns:
	movieID from IMDb SQL database corresponding to correct movie.
	'''
	for x in movies:
		ia.update(x)
		# print x['year']
		if 'year' in x.keys():
			# if x['kind'] == 'movie' or x['kind'] == 'video movie':
			# print x, x['kind'], x['year'], year
			# if ['kind'] in x:
			# 	print 'we have a type'
			if x['kind'] == 'movie' and int(x['year']) == int(year):	
				return x.movieID

			elif x['kind'] == 'video movie' and int(x['year']) == int(year):
				return x.movieID

			elif x['kind'] == 'tv series' and int(x['year']) == int(year):
				return x.movieID

lang_id = 'http://api.netflix.com/categories/languages'
audio_id = 'http://api.netflix.com/categories/audio'

with open('movies_full.xml', 'rt') as f:
	with open("netflix.csv", "wb") as out1:
		with open("lang.csv", "wb") as out2:
			with open("audio.csv", "wb") as out3:
				sw1 = csv.writer(out1, delimiter=',',quotechar='"', escapechar='\\')#, quoting=csv.QUOTE_NONE)
				sw2 = csv.writer(out2, delimiter=',')#, quotechar="")
				sw3 = csv.writer(out3, delimiter=',')#, quotechar="")
				sw1.writerow(['movieID', 'title', 'year', 'rating', 'DVDfrom', 'DVDuntil', 'instantFrom', 'instantUntil', 'language', 'audio', 'runtime'])
				sw2.writerow(['movieID', 'year', 'language'])
				sw3.writerow(['movieID', 'year', 'audio format'])

				for action, elem in etree.iterparse(f):
					# print ("%s: %s: %s" % (elem.tag, elem.attrib, elem.text)) 

					if elem.tag == 'id':

						mID, title, year, rating, DVDfrom, DVDuntil, instantFrom, instantUntil, language, audio, runtime = (None, None, None, None, None, None, None, None, None, None, None)
						entry = [mID, title, year, rating, DVDfrom, DVDuntil, instantFrom, instantUntil, language, audio, runtime]

					if 'label' in elem.attrib:
						label = elem.attrib['label']
						# print "LABEL = " + label
					# print elem.tag
					if elem.tag == 'title':
						title = elem.attrib['regular']
						print title
					elif elem.tag == 'release_year':
						year = elem.text
					elif elem.tag == 'average_rating':
						rating = elem.text
					elif elem.tag == 'availability':
						if label == 'DVD':
							# print "DVD LABEL"
							if 'available_from' in elem.attrib and DVDfrom is None:
								DVDfrom = elem.attrib['available_from']
							# print DVDfrom
							if 'available_until' in elem.attrib:
								DVDuntil = elem.attrib['available_until']
						if label == 'instant':
							if 'available_from' in elem.attrib and instantFrom is None:
								instantFrom = elem.attrib['available_from']
							if 'available_until' in elem.attrib:
								instantUntil = elem.attrib['available_until']
					elif elem.tag == 'category' and elem.attrib['scheme'] == lang_id:
						lang = elem.attrib['label']
						if language is None:
							language = [lang]
						else: 
							if lang not in language:
								language.append(lang)

						# print "LANG = " + language
					elif elem.tag == 'category' and elem.attrib['scheme'] == audio_id:
						currAudio = elem.attrib['label']
						if audio is None:
							audio = [currAudio]
						else:
							if currAudio not in audio:
								audio.append(currAudio)
					elif elem.tag == 'runtime':
						runtime = elem.text

					if elem.tag == 'catalog_title':	
						# print 'true title ' + title
						# movies = ia.search_movie(title)
						# mID = correctID(movies, year)

						title = title.encode('ascii','ignore')

						title = title.replace(",","")

						entry = [title, year, rating, DVDfrom, DVDuntil, instantFrom, instantUntil, runtime, language, audio]
						# print entry
						data = entry

						# if data[0].startswith('\''):
						# 	data[0] = data[0][1:-1]

						print data[:8]
						sw1.writerow(("\"%s\"" % data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
						if data[8] is not None:
							for x in range(len(data[8])):
								print '\"%s\"' % (data[0]), data[1], data[8][x]
								sw2.writerow(('\"%s\"' % data[0], data[1], data[8][x]))
						if data[9] is not None:
							for y in range(len(data[9])):
								print '\"%s\"' %data[0], data[1], '\"%s\"' %data[9][y]
								sw3.writerow(('\"%s\"' %data[0], data[1], '\"%s\"' %data[9][y]))

						print "--------------------------------"