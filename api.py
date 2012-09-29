from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import tweepy
import os

from secrets import *
from config import *
import brains

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
			

class TestOut(webapp.RequestHandler):
	def get(self):
		country = self.request.GET.get('country')
		tweet = {
			"to": [],
			"countries": [country],
			"hashtags": ['#tariffbot']
		}
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(brains.compose(configobject['lexicon'][0], tweet))

application = webapp.WSGIApplication(
	[
		('/tweet', Tweet),
		('/tasks/search', Search),
		('/testout', TestOut),
	],
	debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()