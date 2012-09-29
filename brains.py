import config
import random
import urllib2
import json
import os
import math
import countryinfo
import tweepy
from secrets import *

def t_con():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return tweepy.API(auth)


def getIndicatorValue(country, indicator):
	val = False
	response = urllib2.urlopen(config.configobject['wb_indicator_url'].format(country=country, indicator=indicator))
	data = json.loads(response.read())
	for year in data[1]:
		cand = year['value']
		if cand:
			try:
				val = math.ceil(float(cand))
			except:
				val = cand
			break;
	return val

def codeForCountry(country):
	for co in countryinfo.countries:
		if co['name'] == country:
			return co['code']

def makeVisLink(tweet):
	cos = ";".join([codeForCountry(x) for x in tweet.countries])
	url = config.configobject['vis_url'].format(country=cos, indicator=tweet.spec['relevant_data'][1])
	return url

def compose(tweet):
	template = random.choice(tweet.spec['response_templates'])
	value = getIndicatorValue(codeForCountry(tweet.countries[0]), tweet.spec['relevant_data'][1])
	if value:
		out = template.format(country=tweet.countries[0], value=value)
		if tweet.tags:
			out += ' ' + ' '.join(tweet.tags)
		out += ' ' + makeVisLink(tweet)
		return tweet.respond and '@' + tweet.from_user + ' ' + out or out
	else:
		return False #We can't make a tweet :-(

def send(text):
	if text:
		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):
			t_con().update_status(text)
		return "{text}".format(text=text)
	else:
		return "nothing... :-("


def parse(spec, tweets):
	for tweet in tweets:
		tweet.text = tweet.text.lower()
		tweet.words = set(tweet.text.split(' '))
		tweet.stemmedwords = tweet.words.union(set(word[:-1] for word in tweet.words if word.endswith('s'))) #a horrible hack instead of stemming
		tweet.tags = set(word for word in tweet.words if word.startswith('#'))
		tweet.users = set(word for word in tweet.words if word.startswith('@'))
		tweet.countries = [country[0] for country in config.configobject["countries"] if country[1].issubset(tweet.words)]	
		tweet.spec = spec

	return tweets

def select(tweets):
	outtweets = []
	for tweet in tweets:
		interesting = True

		# EXCLUSIONS FIRST!
		if not len(tweet.countries):
			continue

		for synonyms in tweet.spec["search_criteria"]:
			if not tweet.stemmedwords.intersection(synonyms): 
				interesting = False
				break

		if interesting:
			outtweets.append(tweet)
		else:
			print "rejected: ", tweet
	return outtweets


	

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
		Tweet("could be @dpinsen bashing seems tendentious. an assertive trade policy can encourage investment no? e.g., reagan's japan tariff threats?"),
		Tweet("this shouldn't get through the #test"),
		Tweet("united arab emirates trade tariffs"),
		]
	for tweet in select(parse(testspec, tweets)):
		print "text: ", tweet.text
		print "words: ", tweet.words
		print "stemmedwords: ", tweet.stemmedwords
		print "tags: ", tweet.tags
		print "users: ", tweet.users
		print "countries: ", tweet.countries
		print

