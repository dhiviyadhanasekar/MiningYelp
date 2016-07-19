#!/usr/bin/env python
import db_reviews as db 
import re

import text_parsing as tp
import gram_stopwords
from stopwords import stopwords
one_gram_stopwords = gram_stopwords.one_gram_stopwords
two_gram_stopwords = gram_stopwords.two_gram_stopwords

def convert_to_words(text):
  return re.sub(r'\W+', ' ', text.lower())

def process_businesses(limit):
  businesses = db.get_db_business_data(limit)
  for bus in businesses:
    bus_name = convert_to_words( bus[2] )
    bus_categories = convert_to_words( bus[1] )
    bus_id = bus[0]
    print ''
    print 'Processing Business - ' + bus_id, ' ', bus_name
    #print 'Catgories: ', bus_categories 
    process_bus(bus_id, bus_categories, bus_name)

# stem(phrase, stem_map):
def get_popular_map(popular_foods, stem_map):
  popular_map = {}
  for food in popular_foods:
    food_name = food[0]
    food_name = tp.stem(food_name, stem_map)
    if food_name in one_gram_stopwords or food_name in two_gram_stopwords or food_name in stopwords: continue
    if food_name in popular_map: popular_map[food_name] += food[1]
    else: popular_map[food_name] = food[1] 
  # print popular_map
  return popular_map 


def process_bus(bus_id, bus_categories, bus_name):
  reviews = db.get_db_reviews(bus_id, ''); #db.get_db_reviews('d_8bMNQd0mesbEUeq1U2kQ', 10);
  if len(reviews) == 0: return
  try:
    process_popular_foods(bus_id, bus_categories, bus_name, reviews)
    update_reviews_processed(bus_id, reviews)
  except Exception,e: print 'BBB Got an error code:', str(e)

def process_popular_foods(bus_id, bus_categories, bus_name, reviews):
  popular_foods = db.fetch_popular_foods(bus_id, '')
  stem_map = {}
  popular_map = get_popular_map(popular_foods, stem_map)
  if len(reviews) > 0: tp.loop_reviews(reviews, bus_categories, bus_name, popular_map, stem_map)
  update_db(popular_map, bus_id)

def update_reviews_processed(bus_id, reviews):
    # for r in reviews:
      # db.mark_review_processed(bus_id, r[1])
      db.mark_all_review_processed(bus_id)

def update_db(popular_map, bus_id):
  db.delete_popular_foods(bus_id)
  if(len(popular_map) == 0): return
  sql = "INSERT INTO `bus_popular_foods` (`business_id`, `food_name`, `score`) VALUES"
  for food in popular_map:
    sql += " ('"+ bus_id +"', '"+ food +"', "+ str(popular_map.get(food)) +")," 
  sql = sql[:-1]
  sql += ";"
  print sql
  db.update_all_popular_foods(sql)
    # print food + ' ' + str(popular_map.get(food))
    # db.update_popular_foods(bus_id, food, popular_map.get(food))


def migrate_old_data(limit):
  businesses = db.get_food_db_business_data(limit)
  for bus in businesses:
      print ''
      print 'Processing Business - ' + bus[0], ' ', bus[2]
      process_popular_foods(bus[0], '', '', [])

# update_db({'abc': 1}, '1234')
process_businesses('')
# migrate_old_data('')
