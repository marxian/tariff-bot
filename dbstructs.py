from google.appengine.ext import db


class TweetParent(db.Model):
	pass


class TweetDbEntry(db.Model):
	message = db.StringProperty(required = True)
	response = db.StringProperty()

tweetparent = TweetParent(key_name = "test")
parentkey = tweetparent.key()
if not TweetParent.get(parentkey):
	tweetparent.put()
	