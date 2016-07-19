#!/usr/bin/env python
import text_parsing as tp

review_text = "I'm not a bagel connoisseur, but sometimes I get a hankering for a round dough bread ring with salty spread on it, and when I get that craving I go here. I like any of the savory bagels with the salmon schmear. It's all good. A lot of the other reviews complain about the service; I've never had a problem. If you want a bagel, and you're nearby, come here. Food is spicy"

# review_text = 'if star of india soi is named after the historic ship that set sail from great britain to india then it is best to declare at the beginning that there is nothing worth remembering about this place and there is little that keeps you afloat in the morass of ordinary fare. like many other indian restaurants in the valley the smell of indian cooking hangs in the air and permeates every piece of furnishing. the place does not disappoint when it comes to service it is warm quick and attentive. the complimentary papadums indian flatbread with homemade chutneys condiments is usually the high point of a meal at soi. experiences with the order could be as follows gobi parantha indian bread stuffed with cauliflower the real thing is meant to be fluffy and served with butter but the soi parantha resembles a toppingless thin crust pizza. lamb korma the gravy is thick nutty with a lot of authentic flavours but the meat tastes precooked. chicken biriyani it is difficult to describe the godfood that is biryani but soi manages to serve a new variation which is nothing more than chicken pieces thrown into a mishmash of rice and vegetables. disheartenment with the overpriced substandard food could lead to a decision of not ordering dessert. finally as observed in other reviews and the menu if you visit this place then stick with the tandoori stuff and chefs specialities. however in that case the excitement of an extensive menu will be lost.'

# tp.process_review(review_text.lower(), tp.get_cuisine_words(), {})
# process_review(review_text, cuisine_words, popular_map, popular_words, skipped_words, business_name, stars, stem_map):
popular_map = {}
cuisine_words = tp.get_cuisine_words('american')
popular_words = {}
skipped_words ={}
stem_map ={}

tp.process_review(review_text.lower(), cuisine_words , popular_map, popular_words, skipped_words, '', 5, stem_map)
tp.process_review('savory bagel', cuisine_words, popular_map, popular_words, skipped_words, '', 5, stem_map)
tp.print_popular_items(popular_map)
