#!/usr/bin/env python
from __future__ import division
import db_reviews as db 
import wiki_api as wiki
import gram_stopwords


import string
from operator import itemgetter
import nltk
from nltk.corpus import wordnet as wn
from stopwords import stopwords
one_gram_stopwords = gram_stopwords.one_gram_stopwords
start_word_stopwords = gram_stopwords.start_word_stopwords
two_gram_stopwords = gram_stopwords.two_gram_stopwords
exclude = set(string.punctuation)


def get_file_words(filename, wn_map):
	with open(filename,'r') as f:
		for line in f:
			for word in line.split():
				wn_map[word.lower()] = 1 
	#print(wn_map)
	return wn_map

def is_wn_food(word, index, pos_tag):
	word_synsets = wn.synsets(word, wn.NOUN)
	food_synset1 = wn.synset('food.n.01')
	food_synset2 = wn.synset('food.n.02')
	for synset in word_synsets:
		 hypernyms = synset.lowest_common_hypernyms(food_synset1)
		 hypernyms.extend(synset.lowest_common_hypernyms(food_synset2))
		 #print(word , '------->', hypernyms)
		 for h in hypernyms:
				if h.name().split('.')[0] == 'food':
					#print 'adding [' + str(index) + '] ------- ' + word + ', wn_foods ' + pos_tag
					return True
	return False

def is_wiki_food(word, index, pos_tag):
	if wiki.is_wiki_api_food(word):
		#print 'adding [' + str(index) + '] ------- ' + word + ', wiki ' + pos_tag 
		return True
	return False

def is_local_hash_cuisine(word, cuisine_map, index, pos_tag):
	if word in cuisine_map:
		#print 'adding [' + str(index) + '] ------- ' + word + ', cuisine_words map ' + pos_tag
		return True
	return False


def stem(phrase, stem_map):

	phrase_array = phrase.split(' ')
	word = phrase_array[len(phrase_array)-1]
	stemmed_word = wn._morphy(word, 'n')
	if len(stemmed_word) > 0:
		stemmed_word = stemmed_word[len(stemmed_word)-1]
		if stemmed_word in stem_map: word = stem_map.get(stemmed_word)
		else: stem_map[stemmed_word] = word
		phrase_array[len(phrase_array)-1] = word
		return ' '.join(phrase_array)
	else: return phrase



def add_word_to_popular_map(popular_map, word, current_map, stars, stem_map, phrase_word_count):

	if(phrase_word_count == 1 and (word in one_gram_stopwords or len(word) <= 1 )):
		return

	if(phrase_word_count == 2 and word in two_gram_stopwords): return

	word = stem(word, stem_map)
	if word in current_map:
		return
	current_map[word] = 1

	if word in popular_map:
		popular_map[word] += stars
	else:
		popular_map[word] = stars


def is_word_already_food(word, popular_words, index, pos_tag):
	if word in popular_words:
		#print 'adding [' + str(index) + '] ------- ' + word + ', popular_words '+ pos_tag
		return True
	return False


def get_filtered_words(filtered_words, word_list, cuisine_words, popular_map,  popular_words, skipped_words, business_name, stars, stem_map):
	
	prev_word_index = -1
	prev_word = '' 
	space = ''
	filtered_words = []
	current_map = {}
	phrase_word_count = 0

	for index, word_array in enumerate(word_list):
		
		word = word_array[0]
		pos_tag = word_array[1]
		word = ''.join(ch for ch in word if ch not in exclude)
		
		if len(word) == 0: continue    
		
		if word.isdigit() or word in stopwords or word in skipped_words: #or word in business_name:
			#print 'skipped (stopword) ---' + word
			continue
		
		if is_word_already_food(word, popular_words, index, pos_tag) \
				or is_local_hash_cuisine(word, cuisine_words, index, pos_tag) \
				or is_wn_food(word, index, pos_tag) \
				or is_wiki_food(word, index, pos_tag):

			#add_word_to_popular_map(popular_map, word, -1)
			popular_words[word] = 1
			if prev_word_index == index-1 or prev_word_index == -1:
				prev_word_index = index
				if phrase_word_count == 1 and prev_word in start_word_stopwords:
					prev_word = word
					phrase_word_count = 1
				else:
					prev_word += space + word
					space = ' '
					phrase_word_count += 1
			else:
				filtered_words.append(prev_word)
				add_word_to_popular_map(popular_map, prev_word, current_map, stars, stem_map, phrase_word_count)
				prev_word_index = index
				prev_word = word
				phrase_word_count = 1
		
		else:
			skipped_words[word] = 1 
			#print('skipped ['+ str(index) +'] ---', word, ', ', word_array[1])
	
	if prev_word_index != -1:
		filtered_words.append(prev_word)
		add_word_to_popular_map(popular_map, prev_word, current_map, stars, stem_map, phrase_word_count )
	return filtered_words


def get_cuisine_words(categories):
	cuisine_words = {}

	get_file_words('General_Cuisine.txt', cuisine_words)
	if 'indian' in categories: get_file_words('Indian_Cuisine.txt', cuisine_words)
	if 'american' in categories: get_file_words('American_Cuisine.txt', cuisine_words)
	#print cuisine_words
	return cuisine_words


def update_skipped_words(skipped_words, categories):
	for word in categories:
		skipped_words[word] = 1


def loop_reviews(reviews, categories, business_name, popular_map, stem_map):
	
	# popular_map = {}  
	business_name = business_name + ' ' + categories
	cuisine_words = get_cuisine_words(business_name)
	popular_words = {}
	skipped_words = {}
	# stem_map = {}
	# update_skipped_words(skipped_words, categories)

	for review_count, review in enumerate(reviews):
		review_text = review[0].replace('<single>', "'")
		stars = review[2] #+ 0.5*(review[3] + review[4] + review[5])
		process_review(review_text, cuisine_words, popular_map, popular_words, skipped_words, business_name, stars, stem_map)
		#print('************* End of review '+ str(review_count) +': ' + review[1] + ' stars=' + str(stars) + ' *******************')
		#print ' '
	print_popular_items(popular_map)

	 
def process_review(review_text, cuisine_words, popular_map, popular_words, skipped_words, business_name, stars, stem_map):
	#print 'review_text ======= ' + review_text
	words_to_tag = nltk.word_tokenize(review_text)
	word_list = nltk.pos_tag(words_to_tag)

	filtered_words = get_filtered_words([], word_list, cuisine_words, popular_map,  popular_words, skipped_words, business_name, stars, stem_map)

	#print(filtered_words)
	#print('COUNT::::', len(filtered_words))
	#print('popular map: ', popular_map);



def print_popular_items (popular_map):
	print ' '
	print '~~~~~~~~~~~~~~~~~~~~~ Popular Items ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	sorted_popular_items = sorted(popular_map.items(), key=itemgetter(1), reverse=True)
	for item in sorted_popular_items:
			print item[0], ' ', item[1]
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print ' '



# reviews = db.get_db_reviews('d_8bMNQd0mesbEUeq1U2kQ', 10, [], []);
# loop_reviews(reviews)

