configobject = {

	"lexicon" : [

		{
		"twitter_search_term" : "trade tariff",
		"search_criteria" : [["trade", "imports"],["tariffs", "embargoes"]],
		"relevant_data" : ("Imports of goods and services (% of GDP)", 'NE.IMP.GNFS.ZS'),
		"response_templates" : ["Import tariffs in #{country} are {value}%", "There is a {value}% level of import tax in #{country}"],
		}


	],
	"wb_indicator_url": "http://api.worldbank.org/countries/{country}/indicators/{indicator}?per_page=10&date=2006:2015&format=json"


}