import countryinfo
configobject = {

	"lexicon" : [
		{
			"twitter_search_term" : "trade tariff",
			"search_criteria" : [["trade", "import"],["tariff", "embargo"]],
			"relevant_data" : ("Imports of goods and services (% of GDP)", 'NE.IMP.GNFS.ZS'),
			"response_templates" : ["Import tariffs in {country} are {value}%", "There is a {value}% level of import tax in {country}"]
		}
	],
	"wb_indicator_url": "http://api.worldbank.org/countries/{country}/indicators/{indicator}?per_page=10&date=2006:2015&format=json",
	"vis_url": "http://dev.wetoffice.com/form.html?country={country}&indicator={indicator}"
}


#countries gets transformed to the format (string, set) here
countries = [x['name'] for x in countryinfo.countries]
for i in range(len(countries)):
	countries[i] = (countries[i], set(countries[i].lower().split(' ')))
configobject['countries'] = countries

if __name__ == '__main__':
	print configobject
