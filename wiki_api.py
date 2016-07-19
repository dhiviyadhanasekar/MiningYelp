#!/usr/bin/env python
import string
from urllib2 import Request, urlopen, URLError
import json
import nltk
from nltk.corpus import wordnet as wn
import re

wiki_text_search_words = ['food', 'foods', 'dish', 'dishes']

def strip_extract(extract):
  data = extract
  data = data.replace('-', ' ')
  data = ' '.join(data.split())
  data = re.sub('[^a-z ]', '' ,data.lower()) 
  extract_words = data.split()
  return extract_words

def is_word_in_extract(extract_words, word):
  for eword in extract_words:
    if word == eword: return True
  return False

def is_wiki_api_food(phrase):

  if len( wn.synsets(phrase) ) != 0:
    return False

  # print 'checking wiki for ' + phrase

  request = Request('https://en.wikipedia.org/w/api.php?action=query&prop=extracts|info&exintro&exlimit=max&inprop=url&generator=search&gsroffset=&format=json&gsrsearch='+ phrase +'&redirects&continue=')
  
  try:
    response = urlopen(request)
    wiki_text = json.loads(response.read().decode("utf8"))

    if 'query' not in wiki_text or 'pages' not in wiki_text['query']: return False
    wiki_pages = wiki_text['query']['pages']
    
    for pageIds in wiki_pages:

      wiki_title = wiki_pages[pageIds]['title']
      wiki_extract = wiki_pages[pageIds]['extract']
      stripped_extract = strip_extract(wiki_extract)

      for word in wiki_text_search_words:
        # if (phrase in wiki_title or '<b>'+phrase+'</b>' in wiki_extract) and word in wiki_extract:  
        if (phrase in wiki_title or '<b>'+phrase+'</b>' in wiki_extract) and is_word_in_extract(stripped_extract, word):  
          print word + ' found in wiki page - ' + wiki_title
          return True

  except Exception,e: print 'Not wiki phrase -'+ phrase +'. Got an error code:', str(e)
  
  return False

# print is_wiki_api_food('tikka')

