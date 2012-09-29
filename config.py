configobject = {

	"lexicon" : [

		{
		"twitter_search_term" : "trade",
		"search_criteria" : [["trade", "import"],["tariff", "embargo"]],
		"relevant_data" : [],
		"response_templates" : ["Import tarrifs in {country} are {value}", "There is a {value} level of import tax in {country}"],
		},
		{
		"twitter_search_term" : "electricity access",
		"search_criteria" : [["access", "availability"], ["power", "electricity"]],
		"relevant_data" : [],
		"response_templates" : ["{value} of people have access to power in {country}"],
		}
	],

	"countries" : [ #canonical name
		"Great Britain",
		"United Arab Emirates"
	
	]
	

}

#countries gets transformed to the format (string, set) here
countries = configobject["countries"]
for i in range(len(countries)):
	countries[i] = (countries[i], set(countries[i].lower().split(' ')))

if __name__ == '__main__':
	print configobject