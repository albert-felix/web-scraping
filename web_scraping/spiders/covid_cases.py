import scrapy
from collections import defaultdict
import pandas as pd

class CovidCases(scrapy.Spider):
    name = "covid-cases"
    start_urls = [
        "https://www.worldometers.info/coronavirus/"
    ]

    def parse(self, response):
        records = response.xpath('//table[@id="main_table_countries_today"]/tbody/tr')
        result = defaultdict(list)
        # Scraping table data
        for record in records:
            row = record.css('td')
            country = row.xpath('string(self::*)').extract()[1]
            totalCases = row.xpath('string(self::*)').extract()[2]
            newCases = row.xpath('string(self::*)').extract()[3]
            totalDeaths = row.xpath('string(self::*)').extract()[4]
            totalRecovered = row.xpath('string(self::*)').extract()[6]
            activeCases = row.xpath('string(self::*)').extract()[8]

            # Appending data to dict
            result['country'].append(country)
            result['totalCases'].append(totalCases)
            result['newCases'].append(newCases)
            result['totalDeaths'].append(totalDeaths)
            result['totalRecovered'].append(totalRecovered)
            result['activeCases'].append(activeCases)

        df = pd.DataFrame(result)
        # Dropping rows with Continents and Total Counts (only has country specific data)
        country_df = df.iloc[7:229]
        country_df.reset_index(inplace=True, drop=True)
        print(country_df.head())
