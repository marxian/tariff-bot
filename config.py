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
		"great britain",
	
	]
	

}
countries = configobject["countries"]
for i in range(len(countries)):
	countries[i] = set(countries[i].split(' '))

print configobject