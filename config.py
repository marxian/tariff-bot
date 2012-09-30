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
			"search_criteria" : [["population", "people"],["total","number"]],
			"relevant_data" : ("Total Population", 'SP.POP.TOTL'),
			"response_templates" : ["The population of {country} is {value}", "There are {value} people living in {country}"]
		},
		{
			"twitter_search_term" : "life",
			"search_criteria" : [["life","lifetime","age"],["expectancy","average"]],
			"relevant_data" : ("Life expectancy at birth", 'SP.DYN.LE00.IN'),
			"response_templates" : ["The life expectancy of someone in {country} is around {value}", "On average, people in {country} live to {value} years old"]
		}

	],
	"wb_indicator_url": "http://api.worldbank.org/countries/{country}/indicators/{indicator}?per_page=10&date=2006:2015&format=json",
	"vis_url": "http://dev.wetoffice.com/form.html?country={country}&indicator={indicator}"
}


#countries gets transformed to the format (string, set) here
countries = [" ".join((x['name'], x['code'])) for x in countryinfo.countries]
for i in range(len(countries)):
	countries[i] = (countries[i], set(countries[i].lower().split(' ')).union())
configobject['countries'] = countries

if __name__ == '__main__':
	print configobject
