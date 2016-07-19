#!/usr/bin/env python
import nltk
from nltk.corpus import wordnet as wn
def common_hypernym():
  synset1 = wn.synset('chutney.n.01')
  synset2 = wn.synset('food.n.01')
  input_str = ''
  while(input_str != 'exit'):
        input_str = raw_input('Enter: ')
        for synset1 in wn.synsets(input_str, wn.NOUN):
            print( synset1.lowest_common_hypernyms(synset2))

def food_names(food_synsets):
  for synset in food_synsets:
    print( synset.name().split('.')[0] )
    hyponyms = synset.hyponyms()
    food_names(hyponyms)

#print(wn.synsets('chutneys'))
common_hypernym()

food_synsets = []
food_synsets.append(wn.synset('food.n.01'))
food_synsets.append(wn.synset('food.n.02')) 
#food_names(food_synsets)

#for synset in wn.synset('food.n.01').hyponyms():
#	print(synset)

def common_hypernym():
  synset1 = wn.synset('chutney.n.01')
  synset2 = wn.synset('food.n.01')
  input_str = ''
  while(input_str != 'exit'):
  	input_str = raw_input('Enter: ')
        for synset1 in wn.synsets(input_str, wn.NOUN):
    	    print(synset1, synset1.lowest_common_hypernyms(synset2))
    


#for synset in list(wn.all_synsets('n')):
 # synname = synset.name().split('.')[0]
 # if('food' == synname):
 #  print(synset)

#for synset in wn.all_synsets('n'):
#	synname = synset.name().split('.')[0]
#	if('pasta' in synname): 
#		print(synset, synset.hypernyms)


