'''
Karl Shiffler (shiffler@bu.edu)

Script iterates through individual rating data from the Netflix Prize data.
Must be run in the same directory as filenames.txt (a simple list of all the filenames) and movie_titles.txt

'''

from lxml import etree #import iterparse
import numpy as np
import cPickle as pickle
from imdb import IMDb 
import csv

ratingID = 0

with open("filenames.txt" ,'rb') as infile:
	with open("ratings.csv", "wb") as out:
		with open("movie_titles.txt", 'rb') as inTitles:
			reader = csv.reader(infile)
			titleReader = csv.reader(inTitles)
			sw = csv.writer(out, delimiter=",")
			sw.writerow(["Rating ID", "Movie ID", "Movie Title", "Movie Year", "Customer ID", "Rating", "Date"])
			
			for fileName, titleInfo in zip(reader, titleReader):
				fullID = fileName[0]
				mID = fullID.replace("mv_", "")
				mID = mID.replace(".txt", "")
				mID = mID.lstrip("0")
				year = titleInfo[1]
				title = titleInfo[2]

				with open("./training_set/%s" %fullID, "rb") as ratings:
					ratingReader = csv.reader(ratings)
					ratingReader.next()
					for row in ratingReader:
						data = [ratingID, mID, title, year]
						data.extend(row)
						sw.writerow(data)
						ratingID += 1
				
				print fullID," ", mID, " ", year, " ", title