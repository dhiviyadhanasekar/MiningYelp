#!/usr/bin/env python
import MySQLdb

def connect_db():
  return MySQLdb.connect("localhost","root","sjsu123", "yelp_db")

def mark_review_processed(business_id, review_id):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "update review1 set processed = 1 where business_id = '"+business_id+"' and review_id='" + review_id+ "'"
  print "query:" + sql
  cursor.execute(sql)
  db.commit()
  db.close()

def mark_all_review_processed(business_id):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "update review1 set processed = 1 where business_id = '"+business_id+"'"
  print "query:" + sql
  cursor.execute(sql)
  db.commit()
  db.close()

def update_all_popular_foods(sql):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  # sql = "insert into bus_popular_foods (business_id, food_name, score) values ('"+ business_id +"', '"+ food_name +"', "+ str(score) +")"
  # print sql
  cursor.execute(sql)
  db.commit()
  db.close()

def update_popular_foods(business_id, food_name, score):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "insert into bus_popular_foods (business_id, food_name, score) values ('"+ business_id +"', '"+ food_name +"', "+ str(score) +")"
  # print sql
  cursor.execute(sql)
  db.commit()
  db.close()


def delete_popular_foods(business_id):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "delete from bus_popular_foods where business_id = '"+ business_id + "'"
  # print sql
  cursor.execute(sql)
  db.commit()
  db.close()



def fetch_popular_foods(business_id, limit):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "select food_name, score from bus_popular_foods where business_id = '" + business_id +"' order by score desc"
  strLimit = str(limit)
  if strLimit.isdigit(): sql = sql + " limit " + strLimit 
  cursor.execute(sql)
  results = cursor.fetchall()
  # print results
  db.close()
  return results



def get_db_reviews(business_id, limit): 
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "select reviewtext, review_id, stars, funny, useful, cool from review1 where business_id = '"+ business_id +"' and processed = 0 and stars > 2 order by stars desc"
  strLimit = str(limit)
  if strLimit.isdigit(): sql = sql + " limit " + strLimit 
  cursor.execute(sql)
  results = cursor.fetchall()
  # print len(results)
  db.close()
  return results


def get_food_db_business_data(limit):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "select business_id, categories, name from business where business_id in (select distinct business_id from bus_popular_foods)"
  strLimit = str(limit)
  if strLimit.isdigit(): sql = sql + " limit " + strLimit 
  cursor.execute(sql)
  results = cursor.fetchall()
  # print results
  db.close()
  return results


def get_db_business_data(limit):
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "select business_id, categories, name from business where business_id in (select distinct business_id from review1 where processed = 0 and stars > 2) and id between 13000 and 15000"
  strLimit = str(limit)
  if strLimit.isdigit(): sql = sql + " limit " + strLimit 
  cursor.execute(sql)
  results = cursor.fetchall()
  # print results
  db.close()
  return results

def reset_processing():
  db = connect_db() # db = MySQLdb.connect("localhost","root","sjsu123", "yelp_db")
  cursor = db.cursor()
  sql = "update review1 set processed = 0 where processed = 1"
  #cursor.execute(sql)
  sql = "TRUNCATE TABLE  bus_popular_foods"
  #cursor.execute(sql)
  db.commit()
  db.close()

# get_db_reviews('QbmcCE_cLq4WO8ZMKImaLw', '')
# get_db_business_data(10)
# fetch_popular_foods('QbmcCE_cLq4WO8ZMKImaLw', 1)
# update_popular_foods('QbmcCE_cLq4WO8ZMKImaLw', 'my jbbvjwbvkj', 0)
