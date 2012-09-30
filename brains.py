import config
import random
import urllib2
import json
import os
import math
import countryinfo
from google.appengine.ext import db
import dbstructs
import tweepy
from secrets import *
import string
import re


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
	country = random.choice(list(tweet.countries))
	value = getIndicatorValue(codeForCountry(country), tweet.spec['relevant_data'][1])
	if value:
		out = template.format(country=country, value=value)
		if tweet.tags:
			out += ' ' + ' '.join(tweet.tags)
		out += ' ' + makeVisLink(tweet)
		out = getattr(tweet, 'respond', False) and '@' + tweet.from_user + ' ' + out or out

		#add the response tweet to the db
		dbstructs.TweetDbEntry(key_name = str(tweet.id),
								message = tweet.text,
								response = out,
								parent = dbstructs.parentkey
								).put()
		
		return out
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

		allowed = string.ascii_letters + "@#'" #remove anything not in allowed string
		tweet.words = re.sub(r"[^{allowed}]+".format(allowed = allowed)," ",tweet.text)
		tweet.words = set(tweet.words.split(' '))

		tweet.stemmedwords = tweet.words.union(set(word[:-1] for word in tweet.words if word.endswith('s'))) #a horrible hack instead of stemming
		tweet.stemmedwords = set(s.lower() for s in tweet.stemmedwords)

		tweet.tags = set(word for word in tweet.words if word.startswith('#'))
		tweet.users = set(word for word in tweet.words if word.startswith('@'))
		tweet.countries = set(country['name'] 
							for country in config.configobject["countries"]
							for matchset in country['match_criteria'] 
							if matchset.issubset(tweet.stemmedwords) or matchset.issubset(tweet.words)
							)
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
		key = db.Key.from_path('TweetParent', 'test', 'TweetDbEntry', str(tweet.id))
		if dbstructs.TweetDbEntry.get(key):
			continue #we've already responded or tried to respond to this tweet

		if interesting:
			outtweets.append(tweet)
		else:
			print u"rejected: ", tweet
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

