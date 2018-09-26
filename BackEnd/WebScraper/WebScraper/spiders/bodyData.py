#/home/dtinpa/quirkregistry.com/BackEnd/bin/python2.7
import scrapy
from scrapy import signals
from scrapy import Spider
import sys
from bs4 import BeautifulSoup
import random
import json

# Dana Thompson
# dtdthomp54@gmail.com
# This spider is responsible for gettings a random body part that we may use for the activation of the quirk

# The "Body:" portion helps when reading the spider data.  Since the spiders are ran simultaneously, we can't garuntee order of output.
globalResult = {"Body":"None"}

# This spider is responsible for retrieving a random body part for power activation.
class Spider_BodyData(Spider):
	name = "bodyData";

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(Spider_BodyData, cls).from_crawler(crawler, *args, **kwargs);
		crawler.signals.connect(spider.spider_closed, signals.spider_closed);
		return spider;

	# This website is unique in that the data doesn't load upon visiting the webpage
	# I grabbed the url the button sends a POST request to, and built a form request
	# That mimics the POST request of the button in order to get the data
	def start_requests(self):
		url = 'https://www.getrandomthings.com/data/list-body-parts.php';
		formdata = {
			'num':'6',
			'add':'address',
			'unique':'true',
		};

		req = scrapy.FormRequest(url=url,
			method='POST',
			formdata=formdata,
			callback=self.parse)
		yield req
			#yield scrapy.Request(url=url, callback=self.parse);

	def parse(self, response):
		global globalResult;
		globalResult = {"Body": self.parseBody(response.body)};
	
	# Only prints the final result if the spider ran successfully.
	# Won't indicate if data was unnsuccesfully extracted
	def spider_closed(self, reason):
		if reason == "finished":
			global globalResult;
			print json.dumps(globalResult);
	
	#Parses the html body of the random body site.
	def parseBody(self, response):
		soup = BeautifulSoup(response, 'html.parser');
		bodyList = soup.findAll("div", {"class": "col-md-6"});
		
		result = random.choice(bodyList).get_text().encode("utf-8");
		return result;
