from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import tweepy
import os

import brains
from secrets import *
from config import *

def t_con():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return tweepy.API(auth)

class Tweet(webapp.RequestHandler):
    def get(self):
		api = t_con()
		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):
			api.update_status('Ahem. Testing. Testing. 1, 2, 3...')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Could have tweeted as ' + api.me().name)

class Search(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		api = t_con()
		for spec in configobject['lexicon']:
			self.response.out.write('Twitter search for ' + spec['twitter_search_term'] + '\n')
			results = api.search(spec['twitter_search_term'])
			for result in results:
				self.response.out.write('\t' + result.text + '\n')
				filtertweet(result, spec)
			import pdb
			pdb.set_trace()
			




application = webapp.WSGIApplication(
	[
		('/tweet', Tweet),
		('/search', Search),
	],
	debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()