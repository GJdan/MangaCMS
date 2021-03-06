

from ScrapePlugins.FoolSlide.MangatopiaLoader.FeedLoader    import FeedLoader
from ScrapePlugins.FoolSlide.MangatopiaLoader.ContentLoader import ContentLoader

import ScrapePlugins.RunBase

import time

import runStatus


class Runner(ScrapePlugins.RunBase.ScraperBase):
	loggerPath = "Main.Manga.MngTop.Run"

	pluginName = "MangatopiaLoader"


	def _go(self):

		self.log.info("Checking Mangatopia feeds for updates")
		fl = FeedLoader()
		fl.go()
		fl.closeDB()

		time.sleep(3)
		#print "wat", cl

		if not runStatus.run:
			return

		cl = ContentLoader()

		if not runStatus.run:
			return

		todo = cl.retreiveTodoLinksFromDB()

		if not runStatus.run:
			return

		cl.processTodoLinks(todo)
		cl.closeDB()


if __name__ == '__main__':
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):
		fl = Runner()

		fl.go()

