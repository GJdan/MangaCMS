
import webFunctions

import calendar
import traceback

import settings
import parsedatetime
import urllib.parse
import time

import ScrapePlugins.RetreivalDbBase
class DbLoader(ScrapePlugins.RetreivalDbBase.ScraperDbBase):


	dbName = settings.DATABASE_DB_NAME
	loggerPath = "Main.Manga.NHentai.Fl"
	pluginName = "NHentai Link Retreiver"
	tableKey    = "nh"
	urlBase = "http://nhentai.net/"
	urlFeed = "http://nhentai.net/tagged/english/?page={num}"

	wg = webFunctions.WebGetRobust(logPath=loggerPath+".Web")

	tableName = "HentaiItems"

	def loadFeed(self, pageOverride=None):
		self.log.info("Retreiving feed content...",)
		if not pageOverride:
			pageOverride = 1
		try:
			pageUrl = self.urlFeed.format(num=pageOverride)
			soup = self.wg.getSoup(pageUrl)
		except urllib.error.URLError:
			self.log.critical("Could not get page from NHentai!")
			self.log.critical(traceback.format_exc())
			return None

		return soup


	def getCategoryTags(self, soup):
		tagChunks = soup.find_all('div', class_='field-name')
		tags = []
		category = "None"



		# 'Origin'       : '',  (Category)
		for chunk in tagChunks:
			for rawTag in chunk.find_all("a", class_='tagbutton'):
				if rawTag.span:
					rawTag.span.decompose()
				tag = rawTag.get_text().strip()

				if "Artist" in chunk.contents[0]:
					category = "Artist-"+tag.title()
					tag = "artist "+tag
				tag = tag.replace("  ", " ")
				tag = tag.replace(" ", "-")
				tags.append(tag)

		tags = " ".join(tags)

		return category, tags

	def getUploadTime(self, soup):
		descriptionDiv = soup.find("div", id='info')
		for child in descriptionDiv.children:
			if child.string and "Uploaded" in child.string:
				dateStr = child.string.replace("Uploaded", "").strip()

				# Short circuit for "an hour ago" dates, because
				# parsedatetime fails to parse them.
				if "an hour ago" in dateStr:
					return time.time() - 60*60

				# print(dateStr)
				cal = parsedatetime.Calendar()
				ulDate, status = cal.parse(dateStr)
				# print(dateStr, ulDate, status)
				if status == 0:
					raise ValueError("Invalid date! = '%s'. Return status = '%s'" % (dateStr, status))
				return time.mktime(ulDate)

		raise ValueError("No date found!")

	def getInfo(self, itemUrl):
		ret = {}
		soup = self.wg.getSoup(itemUrl)

		ret["seriesName"], ret['tags'] = self.getCategoryTags(soup)
		ret['retreivalTime'] = self.getUploadTime(soup)

		return ret


	def parseItem(self, containerDiv):
		ret = {}
		ret['sourceUrl'] = urllib.parse.urljoin(self.urlBase, containerDiv.a["href"])

		# Do not decend into items where we've already added the item to the DB
		if len(self.getRowsByValue(sourceUrl=ret['sourceUrl'])):
			return None

		ret.update(self.getInfo(ret['sourceUrl']))

		# Yaoi isn't something I'm that in to.
		if "guys-only" in ret["tags"]:
			self.log.info("Yaoi item. Skipping.")
			return None

		titleTd = containerDiv.find("div", class_='caption')
		ret['originName'] = titleTd.get_text().strip()

		return ret

	def getFeed(self, pageOverride=None):
		# for item in items:
		# 	self.log.info(item)
		#

		soup = self.loadFeed(pageOverride)

		mainDiv = soup.find("div", class_="index-container")

		divs = mainDiv.find_all("div", class_='preview-container')

		ret = []
		for itemDiv in divs:

			item = self.parseItem(itemDiv)
			if item:
				ret.append(item)


		return ret





	def go(self):
		self.resetStuckItems()
		dat = self.getFeed()


		self.processLinksIntoDB(dat)

		# for x in range(10):
		# 	dat = self.getFeed(pageOverride=x)
		# 	self.processLinksIntoDB(dat)



def getHistory():

	run = DbLoader()
	for x in range(1, 1150):
		dat = run.getFeed(pageOverride=x)
		run.processLinksIntoDB(dat)


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=False):
		getHistory()
		# run = DbLoader()
		# run.go()


