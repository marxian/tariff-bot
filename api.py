from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import tweepy
import os
from secrets import * #consumer_key, consumer_secret, access_token and access_token_secret are defined here

class Tweet(webapp.RequestHandler):
    def get(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):
			api.update_status('Ahem. Testing. Testing. 1, 2, 3...')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Could have tweeted as ' + api.me().name)

application = webapp.WSGIApplication(
                                     [('/tweet', Tweet)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()