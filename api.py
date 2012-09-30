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

class Tweet(webapp.RequestHandler):
    def get(self):
		api = brains.t_con()
		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):
			api.update_status('Ahem. Testing. Testing. 1, 2, 3...')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Could have tweeted as ' + api.me().name)

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
			
			#for tweet in results:
			#	self.response.out.write("Saw:\n" + unicode(tweet))

			results = brains.select(results)
			
			for tweet in results:
				self.response.out.write("Would have replied to:\n" + unicode(tweet))
				
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