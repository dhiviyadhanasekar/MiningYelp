#!/usr/bin/env python

import json
import unicodedata
import io

#target = io.open('restaurants.txt', 'w')
target = open('restaurants1.txt', 'w')
sql_insert = "INSERT INTO `business` (`business_id`, `categories`, `review_count`, `name`) VALUES("
quotes = '"'

with open('business_restaurants.json') as data_file:
    for line in data_file:
        csl = []
	pline = sql_insert
        data = json.loads(line)
        #pprint(data['business_id'])
        csl.append(quotes + data['business_id'] + quotes)
        list = []
        for val in data['categories']:
                if val != "Restaurants":
                        list.append(val)
	if list :
        	csl.append(quotes + '-'.join(list) + quotes)
	else:
		csl.append(quotes + 'General' + quotes)
	csl.append(str(data['review_count']))
	csl.append(quotes  + data['name'].replace('\"','') + quotes)
	
        pline = pline + ','.join(csl) + ");"
	print(pline)
	target.write(pline.encode('utf8'))
	#target.write(pline.decode('utf8'))
	#pline = unicodedata.normalize('NFKD',pline.decode('utf-8')).encode('ascii','ignore')
	#target.write(pline)
	target.write("\n")

target.close()
