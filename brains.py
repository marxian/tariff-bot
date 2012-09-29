from config import configobject

def parse(spec, tweets):
	for tweet in tweets:
		tweet.text = tweet.text.lower()
		tweet.words = set(tweet.text.split(' '))
		tweet.stemmedwords = tweet.words.union(set(word[:-1] for word in tweet.words if word.endswith('s'))) #a horrible hack instead of stemming
		tweet.tags = set(word for word in tweet.words if word.startswith('#'))
		tweet.users = set(word for word in tweet.words if word.startswith('@'))
		tweet.countries = [country[0] for country in configobject["countries"] if country[1].issubset(tweet.words)]	

	return tweets

def filter(spec, tweets):
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
		Tweet("embargo import tests tests testing #test @user great britain"),
		Tweet("this shouldn't get through the #test"),
		Tweet("united arab emirates trade tariffs"),
		]
	for tweet in parse(testspec, tweets):
		print "text: ", tweet.text
		print "words: ", tweet.words
		print "stemmedwords: ", tweet.stemmedwords
		print "tags: ", tweet.tags
		print "users: ", tweet.users
		print "countries: ", tweet.countries
		print



		
