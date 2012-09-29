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