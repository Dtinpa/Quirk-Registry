#/home/dtinpa/quirkregistry.com/BackEnd/bin/python2.7
import scrapy
from scrapy import signals
from scrapy import Spider
import sys
from bs4 import BeautifulSoup
import random
import string
import json

# Dana Thompson
# dtdthomp54@gmail.com
# This spider is responsible for gettings a random medical condition to use as a weakness for the power

# The "Body:" portion helps when reading the spider data.  Since the spiders are ran simultaneously, we can't garuntee order of output.
globalResult = {"Weak":"None"}

class Spider_WeakData(Spider):
	name = "weakData";

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(Spider_WeakData, cls).from_crawler(crawler, *args, **kwargs);
		crawler.signals.connect(spider.spider_closed, signals.spider_closed);
		return spider;

	def start_requests(self):
		rLetterLower = random.choice(string.ascii_lowercase);
		url = "https://www.medicinenet.com/symptoms_and_signs/alpha_" + rLetterLower + ".htm"
		yield scrapy.Request(url=url, callback=self.parse);
		
	def parse(self, response):
		global globalResult;
		weak, weakUrl = self.parseBody(response.body);
		globalResult = {"Weak": {
					"Desc": weak,
					"URL": "https://www.medicinenet.com" + weakUrl
				}};
	
	# Only prints the final result if the spider ran successfully.
	# Won't indicate if data was unnsuccesfully extracted
	def spider_closed(self, reason):
		if reason == "finished":
			global globalResult;
			print json.dumps(globalResult);
	
	#Parses the html body of the random body site.
	def parseBody(self, response):
		soup = BeautifulSoup(response, 'html.parser');
		container = soup.find(id="AZ_container");
		listDiv = container.find("ul");
		weakList = listDiv.findAll("li");

		result = random.choice(weakList);
		weakHref = result.find('a', href=True);
		weakUrl = weakHref['href'].encode("utf-8");
		weak = result.get_text().encode("utf-8")
		return weak, weakUrl;
