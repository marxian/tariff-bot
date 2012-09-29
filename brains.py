import config
import random
import urllib2
import json
import math
import countryinfo

def filtertweets(tweets, config = config.configobject):
	pass


def getIndicatorValue(country, indicator):
	val = ':-( unknown'
	response = urllib2.urlopen(config.configobject['wb_indicator_url'].format(country=country, indicator=indicator))
	data = json.loads(response.read())
	cand = False
	for year in data[1]:
		cand = year['value']
		if cand:
			try:
				val = math.ceil(float(cand))
			except:
				val = cand
			break;
	return val


def compose(spec, tweet):
	template = random.choice(spec['response_templates'])
	c_code = [x['code'] for x in countryinfo.countries if x['name'] == tweet['countries'][0]][0]
	value = getIndicatorValue(c_code, spec['relevant_data'][1])
	out = template.format(country=tweet['countries'][0], value=value)
	if tweet['hashtags']:
		out += ' ' + ' '.join(tweet['hashtags'])

	return out


def parse(spec, tweets):
	for tweet in tweets:
		tweet.text = tweet.text.lower()
		tweet.words = set(tweet.text.split(' '))
		tweet.stemmedwords = tweet.words.union(set(word[:-1] for word in tweet.words if word.endswith('s'))) #a horrible hack instead of stemming
		tweet.tags = set(word for word in tweet.words if word.startswith('#'))
		tweet.users = set(word for word in tweet.words if word.startswith('@'))
		tweet.countries = [country[0] for country in config.configobject["countries"] if country[1].issubset(tweet.words)]	

	return tweets

def select(spec, tweets):
	for tweet in tweets:
		interesting = True
		for synonyms in spec["search_criteria"]:
			if not tweet.stemmedwords.intersection(synonyms): 
				interesting = False #these aren't the tweets where looking for

		if interesting: yield tweet


	

if __name__ == '__main__':
	testspec = 	{
		"twitter_search_term" : "trade",
		"search_criteria" : [["trade", "import"],["tariff", "embargo"]],
		"relevant_data" : [],
		"response_templates" : ["Import tarrifs in {country} are {value}", "There is a {value} level of import tax in {country}"],
		}

	class Tweet():
		def __init__(self, text):
			self.text = text

	tweets = [
		Tweet("embargo import tests tests testing #test @user united kingdom"),
		Tweet("this shouldn't get through the #test"),
		Tweet("united arab emirates trade tariffs"),
		]
	for tweet in select(testspec, parse(testspec, tweets)):
		print "text: ", tweet.text
		print "words: ", tweet.words
		print "stemmedwords: ", tweet.stemmedwords
		print "tags: ", tweet.tags
		print "users: ", tweet.users
		print "countries: ", tweet.countries
		print

