from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import tweepy
import os

import brains
from secrets import *
from config import *
import brains

def tweet_to_string(tweet):
	return u"\n".join((
		u"text: " + unicode(tweet.text),
		u"words: " + unicode(tweet.words),
		u"id: " + unicode(tweet.id),
		u"\n",
		))

tweepy.models.SearchResult.__repr__ = tweet_to_string

class Tweet():
	def __init__(self, text):
		self.text = text

class Ask(webapp.RequestHandler):
    def post(self):
		q = self.request.POST.get('q')
		answers = []
		for spec in configobject['lexicon']:
			res = brains.select(brains.parse(spec, [Tweet(q)]))
			for item in res:
				answers.append(brains.compose(item).tariff_bot_says)
		
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(answers))


class Respond(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		api = brains.t_con()
		
		for spec in configobject['lexicon']:
			for_me = api.search(configobject['my_handle'])
			results = brains.parse(spec, for_me)
			results = brains.select(results)
			for tweet in results:
				tweet.respond = True
				self.response.out.write('Tweeted\n')
				self.response.out.write(brains.send(brains.compose(tweet)))
				self.response.out.write('\nIn response to:\n')
				self.response.out.write(tweet.text)
				self.response.out.write('\n')
				self.response.out.write('\n')

class Search(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		api = brains.t_con()
		for spec in configobject['lexicon']:
			self.response.out.write('Twitter search for ' + spec['twitter_search_term'] + '\n')
			results = api.search(spec['twitter_search_term'])

			results = brains.parse(spec, results)

			results = brains.select(results)
			tweeted = []
			for result in results:
				tweeted.append(brains.send(brains.compose(result)))
			
			for tweet in tweeted:
				self.response.out.write('Tweeted\n')
				self.response.out.write(tweet.tariff_bot_says)
				self.response.out.write('\nIn response to:\n')
				self.response.out.write(tweet.text)
				self.response.out.write('\n')
				self.response.out.write('\n')
				
application = webapp.WSGIApplication(
	[
		('/tweet', Tweet),
		('/search', Search),
		('/respond', Respond),
	],
	debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()