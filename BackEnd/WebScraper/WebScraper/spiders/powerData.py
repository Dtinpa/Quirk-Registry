#/home/dtinpa/quirkregistry.com/BackEnd/bin/python2.7
import scrapy
from scrapy import Spider
from scrapy import signals
import sys
from bs4 import BeautifulSoup
import random
import json

# Dana Thompson
# dtdthomp54@gmail.com
# This spider is responsible for retrieving the super power name, desc, and limitations

# Initializing empty json object so it can be accessed anywhere
globalResult = {"Power":"None"}

class Spider_PowerData(Spider):
	name = "powerData"

	# Sets up signals that execute spider functions when triggered, in this case, spider_closed
	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(Spider_PowerData, cls).from_crawler(crawler, *args, **kwargs);
		crawler.signals.connect(spider.spider_closed, signals.spider_closed);
		return spider;

	def start_requests(self):
		urls = [
			'http://powerlisting.wikia.com/wiki/Special:Random',
			]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		limit = self.parseLimit(response.body);
		desc = self.parsePower(response.body);
		special = self.parseSpecialCond(response);
		resultUrl = response.request.url;
                urlSplit = resultUrl.split("/");			

		# Setup the proper json object so it can be turned into a string
		global globalResult;
		globalResult = {"Power": {
				"Name": urlSplit[len(urlSplit) - 1].replace("_", " "),
				"Desc": desc,
				"Limit": limit,
				"Special": special
				}};
				

	# Only prints the final result if the spider ran successfully.
	# Won't indicate if data was unnsuccesfully extracted
	def spider_closed(self, reason):
		if reason == "finished":
			global globalResult;
			print json.dumps(globalResult);


	# Parses the html body of the super power site.  Gets ability name and description.
	def parsePower(self, response):
		soup = BeautifulSoup(response, 'html.parser');
		capabilities = soup.find(id="Capabilities");
		descHtml = capabilities.find_next("p")
		desc = descHtml.get_text();
		
		return desc.encode("utf-8").replace("\n", "");

	# Checks to see if there are Limitations to print, and if there are, return a random one
	def parseLimit(self, response):
		soup = BeautifulSoup(response, 'html.parser');
	
		if soup.find(id="Limitations"):
			limit = soup.find(id="Limitations");
			descHtml = limit.find_next("ul");
			limitList = descHtml.findAll("li");

			weakness = random.choice(limitList).get_text().encode("utf-8");
			return weakness.replace("\n", "");
		else:
			return "None";
			
	# Checks if the power needs a special flag, like "SMART POWERS" won't need a range
	def parseSpecialCond(self, response):
		soup = BeautifulSoup(response.body, 'html.parser');
		resultUrl = response.request.url;
		urlSplit = resultUrl.split("/");		

		if soup.find("li", attrs={"data-name":"Enhancements"}):
			return "No Range";
		elif "Physiology" in urlSplit[len(urlSplit) - 1]:
			return "No Range,body"
		elif soup.find("li", attrs={"data-name":"Smart Powers"}):
			return "No Range,activity"
		else:
			return "None"
