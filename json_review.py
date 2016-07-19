#!/usr/bin/env python
import json
import unicodedata
import string
import re


def remove_accents(data):
        data = data.replace('-', ' ')
        data = ' '.join(data.split())
	return re.sub('[^a-z0-9 \,\.\>\<\!\?\:\;]', '' ,data.lower()) 
#return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

target = open('rev11.txt', 'w')
sql_insert = "INSERT INTO `review1` (`review_id`, `stars`, `reviewtext`, `business_id`, `funny`, `useful`, `cool`) VALUES ("
quotes = '"'

buss_id = {}
with open("buss_id.txt") as f:
    for line in f:
       (key) = line.strip()
       buss_id[key] = 1
#print(buss_id)

with open('review.json') as data_file:
    for line in data_file:
        data = json.loads(line)
	if buss_id.get(data['business_id']) is None: 
		print "not found" + data['business_id']
		continue
	csl = []
	pline = sql_insert
	csl.append(quotes + data['review_id'] + quotes)
	csl.append( str(data['stars']) )
	
	review_text =  data['text'].replace('\"', '')
	review_text = remove_accents(  review_text.replace("'","<single>") )
	csl.append(quotes + review_text + quotes)

	csl.append(quotes + data['business_id'] + quotes)
	csl.append( str(data['votes']['funny']) )
	csl.append( str(data['votes']['useful']) )
	csl.append( str(data['votes']['cool']) )
	
	pline = pline + ','.join(csl) + ");"
	#print(pline)
	
	target.write(pline + "\n")
target.close()

# Running the file generated using this program:
# Dhiviyas-MacBook-Pro:bin dhiviyad$ /usr/local/mysql-5.7.12-osx10.11-x86_64/bin/mysql -u root -p yelp_db < ~/MyApps/MiningYelp/rev11.txt 