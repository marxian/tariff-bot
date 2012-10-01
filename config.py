import countryinfo
configobject = {
	"my_handle": "@tariffbot",
	"lexicon" : [
		{
			"twitter_search_term" : "trade tariff",
			"search_criteria" : [["trade", "import"],["tariff", "embargo"]],
			"relevant_data" : ("Tariff rate applied simple mean all products %", 'TM.TAX.MRCH.SM.AR.ZS'),
			"response_templates" : ["Import tariffs in {country} are {value}%", "There is a {value}% level of import tax in {country}"]
		},
		{
			"twitter_search_term" : "population",
			"search_criteria" : [["population", "people"]],
			"relevant_data" : ("Total Population", 'SP.POP.TOTL'),
			"response_templates" : ["The population of {country} is {value:,.0f}", "There are {value} people living in {country}"]
		},
		{
			"twitter_search_term" : "expectancy",
			"search_criteria" : [["life","lifetime","age"],["expectancy","average"]],
			"relevant_data" : ("Life expectancy at birth", 'SP.DYN.LE00.IN'),
			"response_templates" : ["The life expectancy of someone in {country} is around {value:.0f}", "On average, people in {country} live to {value:.0f} years old"]
		},
		{
			"twitter_search_term" : "unemployment",
			"search_criteria" : [["jobless","unemployment","job","work","labour"]],
			"relevant_data" : ("Total Unemployment", 'SL.UEM.TOTL.ZS'),
			"response_templates" : ["The total unemployment in {country} is {value}%"]
		}


	],
	"wb_indicator_url": "http://api.worldbank.org/countries/{country}/indicators/{indicator}?per_page=10&date=2006:2015&format=json",
	"vis_url": "http://dev.wetoffice.com/form.html?country={country}&indicator={indicator}"
}


#countries gets transformed to the format (string, set) here
configobject['countries'] = []
for country in countryinfo.countries:
	configobject['countries'].append( {
						"name" : country['name'],
						"match_criteria" : ( set(country['name'].lower().split(' ')), set([country['code']]) )
						}
						)

if __name__ == '__main__':
	print configobject
