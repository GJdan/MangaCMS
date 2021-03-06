
import logSetup
if __name__ == "__main__":
	print("Initializing logging")
	logSetup.initLogging()

import TextScrape.SiteArchiver
import webFunctions


class Scrape(TextScrape.SiteArchiver.SiteArchiver):
	tableKey = 'hptytl'
	loggerPath = 'Main.Text.HaruParty.Scrape'
	pluginName = 'HaruPartyScrape'

	wg = webFunctions.WebGetRobust(logPath=loggerPath+".Web")

	threads = 1

	# SELECT COUNT(*) FROM book_items WHERE url LIKE 'https://login.yahoo.com%';
	# SELECT COUNT(*) FROM book_items WHERE url LIKE 'http://b.scorecardresearch.com/%';

	baseUrl = "http://lasolistia.com/haruparty/"
	# startUrl = 'https://docs.google.com/document/d/1ZdweQdjIBqNsJW6opMhkkRcSlrbgUN5WHCcYrMY7oqI'
	# startUrl = 'https://docs.google.com/document/d/1xInAD8v06AIX_urMZRRXHBocDsqBEePMoU1EOTfGRZQ/pub'
	startUrl = 'https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web'
	# startUrl = baseUrl

	feeds = [
		'http://lasolistia.com/haruparty/?feed=rss2'
	]

	# Any url containing any of the words in the `badwords` list will be ignored.
	badwords = [
				"/manga/",
				"/recruitment/",
				"wpmp_switcher=mobile",
				"account/begin_password_reset",
				"/comment-page-",
				'yahoo.com/'
				# Why do people think they need a fucking comment system?
				'/?replytocom=',
				'#comments',

				# Mask out the PDFs
				"-online-pdf-viewer/",
				"like_comment=",
				"_wpnonce=",
				"#comments",
				"#respond",

				# Who the fuck shares shit like this anyways?
				"?share=",
				"scorecardresearch.com/",

				]

	decompose = [
		{'class' : 'site-header'},
		{'id'    : 'site-header'},
		{'id'    : 'secondary'},
		{'class' : 'header-main'},
		{'class' : 'widget-area'},
		{'id'    : 'jp-post-flair'},
		{'class' : 'entry-meta'},
		{'class' : 'post-navigation'},
		{'class' : 'navigation'},
		{'id'    : 'comments'},
		{'class' : 'site-info'},



		{'id'    : 'footer'},
		{'class' : 'site-footer'},
		{'class' : 'photo-meta'},
		{'class' : 'bit'},
		{'id'    : 'bit'},
		{'id'    : 'search-container'},
		{'id'    : 'likes-other-gravatars'},
		{'id'    : 'sidebar'},
		{'id'    : 'carousel-reblog-box'},
		{'id'    : 'infinite-footer'},
		{'id'    : 'nav-above'},
		{'id'    : 'nav-below'},
		{'class' : 'entry-utility'},
		{'name'  : 'likes-master'},

	]

	stripTitle = '| HaruPARTY Translation Group'


	# NEEDS GOOGLE DOC SUPPORT

def test():
	scrp = Scrape()
	scrp.crawl()
	# scrp.retreiveItemFromUrl(scrp.startUrl)


if __name__ == "__main__":
	test()




