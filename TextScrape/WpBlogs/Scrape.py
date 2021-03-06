
import logSetup
if __name__ == "__main__":
	print("Initializing logging")
	logSetup.initLogging()

from TextScrape.WordpressBase import WordpressScrape

import webFunctions


class Scrape(WordpressScrape):
	tableKey = 'wp'
	loggerPath = 'Main.Text.Wp.Scrape'
	pluginName = 'WpScrape'

	wg = webFunctions.WebGetRobust(logPath=loggerPath+".Web")

	IGNORE_MALFORMED_URLS = True
	threads = 10

	baseUrl = [

		'http://fuzionlife.wordpress.com',
		'http://gekkahimethetranslation.wordpress.com',
		'http://gravitytranslations.wordpress.com',
		'http://kobatochandaisuki.wordpress.com',
		'http://lastexorcist.wordpress.com',
		'http://magelifeblog.wordpress.com',
		'http://nanodesutranslations.wordpress.com',
		'http://nightofthehuntingparty.wordpress.com',
		'http://pactwebserial.wordpress.com',
		'http://parahumans.wordpress.com',
		'http://rejecthero.wordpress.com',
		'http://rumorblock.wordpress.com',
		'http://sakurahonyaku.wordpress.com',
		'http://setsuna86blog.wordpress.com',
		'http://shinynewjustice.wordpress.com',
		'http://stcon.wordpress.com',
		'http://stoneburners.wordpress.com',
		'http://taulsn.wordpress.com',
		'http://tieshaunn.wordpress.com',
		'http://tmbrakta.wordpress.com',
		'http://tusjecht.wordpress.com',
		'http://twistedcogs.wordpress.com',
		'http://yoraikun.wordpress.com',
		'https://9ethtranslations.wordpress.com',
		'https://agreyworld.wordpress.com',
		'https://amaburithetranslation.wordpress.com',
		'https://anathemaserial.wordpress.com',
		'https://binhjamin.wordpress.com',
		'https://bluesilvertranslations.wordpress.com',
		'https://choukun.wordpress.com',
		'https://defiring.wordpress.com',
		'https://dlingson.wordpress.com',
		'https://durandaru.wordpress.com',
		'https://endonline.wordpress.com',
		'https://farmerbob1.wordpress.com',
		'https://fateapocryphathetranslation.wordpress.com',
		'https://flickerhero.wordpress.com',
		'https://flowerbridgetoo.wordpress.com',
		'https://fromwhencecamethenamed.wordpress.com',
		'https://fuyuugakuenthetranslation.wordpress.com',
		'https://gargoyleserial.wordpress.com',
		'https://gekkahimethetranslation.wordpress.com',
		'https://gjbuthetranslation.wordpress.com',
		'https://grimgalthetranslation.wordpress.com',
		'https://hajiko.wordpress.com',
		'https://heartcrusadescans.wordpress.com',
		'https://hellotranslations.wordpress.com',
		'https://hendricksensama.wordpress.com/',
		'https://hennekothetranslation.wordpress.com',
		'https://hokagetranslations.wordpress.com',
		'https://hui3r.wordpress.com',
		'https://itranslateln.wordpress.com',
		'https://kamitranslation.wordpress.com',
		'https://kobatochandaisuki.wordpress.com',
		'https://korezombiethetranslation.wordpress.com',
		'https://kurenaithetranslation.wordpress.com',
		'https://kyakka.wordpress.com',
		'https://lorcromwell.wordpress.com',
		'https://loveyouthetranslation.wordpress.com',
		'https://lygartranslations.wordpress.com',
		'https://madospicy.wordpress.com',
		'https://mahoutsuki.wordpress.com',
		'https://manga0205.wordpress.com',
		'https://maoyuuthetranslation.wordpress.com',
		'https://mayochikithetranslation.wordpress.com',
		'https://metalhaguremt.wordpress.com',
		'https://nanodesutranslations.wordpress.com',
		'https://natsutl.wordpress.com',
		'https://neettranslations.wordpress.com',
		'https://netblazer.wordpress.com',
		'https://nightraccoon.wordpress.com',
		'https://ohanashimi.wordpress.com',
		'https://ojamajothetranslation.wordpress.com',
		'https://oniichanyamete.wordpress.com',
		'https://oregairuthetranslation.wordpress.com',
		'https://oreimothetranslation.wordpress.com',
		'https://otterspacetranslation.wordpress.com',
		'https://paztok.wordpress.com',
		'https://pirateyoshi.wordpress.com',
		'https://putttytranslations.wordpress.com',
		'https://reantoanna.wordpress.com',
		'https://rhinabolla.wordpress.com',
		'https://rokkathetranslation.wordpress.com',
		'https://sakurahonyaku.wordpress.com',
		'https://sasamisanthetranslation.wordpress.com',
		'https://scryatranslations.wordpress.com',
		'https://seizonthetranslation.wordpress.com',
		'https://selkinnovel.wordpress.com',
		'https://setsuna86blog.wordpress.com',
		'https://shincodezeroblog.wordpress.com',
		'https://shintranslations.wordpress.com',
		'https://shokyuutranslations.wordpress.com',
		'https://skyworldthetranslation.wordpress.com',
		'https://solitarytranslation.wordpress.com',
		'https://stcon.wordpress.com',
		'https://tensaitranslations.wordpress.com',
		'https://thatguywhosthere.wordpress.com',
		'https://thecatscans.wordpress.com',
		'https://theworsttranslation.wordpress.com',
		'https://tomorolls.wordpress.com',
		'https://tototrans.wordpress.com',
		'https://trippingoverwn.wordpress.com',
		'https://tsaltranslation.wordpress.com',
		'https://tsuigeki.wordpress.com',
		'https://unbreakablemachinedoll.wordpress.com',
		'https://vaancruze.wordpress.com',
		'https://voidtranslations.wordpress.com',
		'https://wartdf.wordpress.com',
		'https://xantbos.wordpress.com',
		'https://yoraikun.wordpress.com',
		'https://zmunjali.wordpress.com',
		'https://kerambitnosakki.wordpress.com',
		'https://aflappyteddybird.wordpress.com',



		# Non explicitly wordpress blogs (that use wordpress internally)
		'http://avertranslation.com',
		'http://giraffecorps.liamak.net',
		'http://gravitytranslations.com',             # The wordpress address redirects to the plain URL
		'http://hellping.org',
		'http://shinsekai.cadet-nine.org',
		'http://worldofwatermelons.com',
		'http://www.taptaptaptaptap.net',
		'http://www.wuxiaworld.com',
		'http://wuxiaworld.com',
		'http://nightbreezetranslations.com',
		'http://www.lingson.com/',

		# This is WP, but it uses an custom theme I haven't tested against.
		'http://arkmachinetranslations.com',

		# Seriously bro, you can change your A record:
		'http://tototr.com',
		'http://tototrans.com',
		'http://totobro.com',

	]


	feeds = [item+"/feed/" for item in baseUrl]


	startUrl = baseUrl
	# startUrl = ['https://bluesilvertranslations.wordpress.com',]
	# startUrl = 'https://docs.google.com/document/d/1RfQP2Hj5JLtzFWy9d1F8kWVfLkjFuVFlTq87yQrOmmI'
	# startUrl = 'https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web'
	# startUrl = 'https://docs.google.com/document/d/1ZdweQdjIBqNsJW6opMhkkRcSlrbgUN5WHCcYrMY7oqI'

	# Any url containing any of the words in the `badwords` list will be ignored.
	badwords = [
				"/manga/",
				"/recruitment/",
				"wpmp_switcher=mobile",
				"account/begin_password_reset",
				"/comment-page-",

				# Why do people think they need a fucking comment system?
				'/?replytocom=',
				'#comments',
				"_wpnonce=",
				'public-api.wordpress.com'
				# Mask out the PDFs
				"-online-pdf-viewer/",

				# Who the fuck shares shit like this anyways?
				"?share=",


				"giraffecorps.liamak.net/pdf/",
				"giraffecorps.liamak.net/contact/",
				"giraffecorps.liamak.net/extras/",
				"wp-comments-post",
				"/page/page/",
				'/feed',

				'rejecthero.wordpress.com',
				'farmerbob1.wordpress.com',
				'pactwebserial.wordpress.com',


				'https://docs.google.com/forms/d',

				]

	decompose = [


		{'class'           : 'authorpost'},
		{'class'           : 'bit'},
		{'class'           : 'blog-feeds'},
		{'class'           : 'blog-pager'},
		{'class'           : 'btop'},
		{'class'           : 'column-left-outer'},
		{'class'           : 'column-right-outer'},
		{'class'           : 'commentlist'},
		{'class'           : 'comments'},
		{'class'           : 'comments-link'},
		{'class'           : 'date-header'},
		{'class'           : 'entry-meta'},
		{'class'           : 'entry-utility'},
		{'class'           : 'footer'},
		{'class'           : 'footer-outer'},
		{'class'           : 'header-outer'},
		{'class'           : 'headerbg'},
		{'class'           : 'komensamping'},
		{'class'           : 'loggedout-follow-normal'},
		{'class'           : 'menujohanes'},
		{'class'           : 'nav-menu'},
		{'class'           : 'navbar'},
		{'class'           : 'photo-meta'},
		{'class'           : 'post-feeds'},
		{'class'           : 'post-footer'},
		{'class'           : 'quickedit'},
		{'class'           : 'sd-content'},
		{'class'           : 'sd-title'},
		{'class'           : 'sidebar'},
		{'class'           : 'tabs-outer'},
		{'class'           : 'widget-area'},
		{'class'           : 'widget-container'},
		{'class'           : 'widget-content'},
		{'class'           : 'wpa'},   # Ads, I think.
		{'class'           : 'wpcnt'},
		{'class'           : 'wpcom-follow-bubbles'},
		{'class'           : 'xoxo'},
		{'class'           : 'meta'},
		{'id'              : 'access'},
		{'id'              : 'bit'},
		{'id'              : 'branding'},
		{'id'              : 'calendar_wrap'},
		{'id'              : 'carousel-reblog-box'},
		{'id'              : 'colophon'},
		{'id'              : 'comments'},
		{'id'              : 'credit-wrapper'},
		{'id'              : 'entry-author-info'},
		{'id'              : 'footer'},
		{'id'              : 'header'},
		{'id'              : 'header-meta'},
		{'id'              : 'headerimg'},
		{'id'              : 'infinite-footer'},
		{'id'              : 'jp-post-flair'},
		{'id'              : 'likes-other-gravatars'},
		{'id'              : 'nav-above'},
		{'id'              : 'nav-below'},
		{'id'              : 'respond'},
		{'id'              : 'secondary'},
		{'id'              : 'sidebar'},
		{'id'              : 'sidebar-wrapper'},
		{'id'              : 'sidebar-wrapper1'}, # Yes, two `sidebar-wrapper` ids. Gah.
		{'id'              : 'site-header'},
		{'id'              : 'site-navigation'},
		{'name'            : 'likes-master'},
		{'style'           : 'display:none'},
		{'role'            : 'banner'},



	]

	decomposeBefore = [


		{'name'  : 'likes-master'},  # Bullshit sharing widgets
		{'class' : 'comments'},
		{'class' : 'comments-area'},
		{'class' : 'wpcnt'},
		{'id'    : 'addthis-share'},
		{'id'    : 'comments'},
		{'id'    : 'info-bt'},
		{'id'    : 'jp-post-flair'},

	]

	stripTitle = [
		"| KobatoChanDaiSukiScan",
		"| Hokage Translations",
		"| 1HP",
		"| Blue Silver Translations",
		"| Krytyk's translations",
		"| Light Novel translations",
		"| LorCromwell",
		"| mahoutsuki translation",
		"| Novel Translation",
		"| TheLazy9",
		"| Tomorolls",
		"| Ziru's Musings",
		'| Gravity translation',
		'| HaruPARTY Translation Group',
		'| Kyakka',
		'| manga0205',
		'| SETSUNA86BLOG',
		'| Solitary Translation',
		'| Sousetsuka',
		'| Tsuigeki Translations',
		'| Unbreakable Machine Doll',
		'| Unlimited Novel Failures',
		'| なのですよ！',
		'| 桜翻訳!',
		'(NanoDesu)',
		'A Translation of the',
		'Roxism HQ |',
		'| SETSUNA86BLOG',
		'mahoutsuki translation |',
		'&#124; Giraffe Corps',
		'| Giraffe Corps',
		'| Shin Sekai Yori &#8211; From the New World',
		'| Shin Sekai Yori - From the New World',
		'| Shin Sekai Yori – From the New World',
		':: tappity tappity tap.',
		'Fanatical |',
		'| Fanatical'

	]


	titleTweakLut = [
		{
			'contain' : ['yuusha party no kawaii ko ga ita no de, kokuhaku shite mita',
			             '告白してみた'],
			'badUrl'  : ['1ljoXDy-ti5N7ZYPbzDsj5kvYFl3lEWaJ1l3Lzv1cuuM'],
			'url'     : 'docs.google.com',
			'add'    : 'Yuusha Party no Kawaii Ko ga ita no de, Kokuhaku Shite Mita - '
		},
		{
			'contain' : ['tang san'],
			'badUrl'  : [],
			'url'     : 'docs.google.com',
			'add'    : 'Douluo Dalu - '
		},
	]

	# Methods to allow the child-class to modify the content at various points.
	def extractTitle(self, srcSoup, doc, url):

		title = doc.title()
		if not title:
			title = srcSoup.title.get_text().strip()

		content = str(srcSoup).lower()
		for tweakDict in self.titleTweakLut:

			# print()
			# print(tweakDict)
			# print()

			# print('contain', any([item.lower() in content.lower() for item in tweakDict['contain']]))
			# print('badUrl', not any([item in url for item in tweakDict['badUrl']]))
			# print('url', tweakDict['url'] in url)

			if any([item in content for item in tweakDict['contain']]) and \
				(not any([item in url for item in tweakDict['badUrl']])) and \
				tweakDict['url'] in url:

				self.log.info("Need to tweak title for url '%s', adding '%s'", url, tweakDict['add'])
				title = tweakDict['add'] + title

		return title

# SELECT title FROM book_items WHERE contents LIKE '%tang san%';

# SELECT title FROM book_items WHERE contents LIKE '%yuusha party no kawaii ko ga ita no de, kokuhaku shite mita%';


	# def checkDomain(self, url):
	# 	return False

	def postprocessBody(self, soup):
		for style_tag in soup.find_all('style'):
			style_tag.decompose()
		for mid_span in soup.find_all("span", _class="c3"):
			mid_span.unwrap()
		return soup

def test():
	scrp = Scrape()
	scrp.crawl()
	# scrp.retreiveItemFromUrl(scrp.startUrl)


if __name__ == "__main__":
	test()




