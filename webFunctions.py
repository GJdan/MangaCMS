#!/usr/bin/python3
import sys
import codecs

import urllib.request, urllib.parse, urllib.error
import os.path

import time
import http.cookiejar

import traceback

import logging
import zlib
import bs4
import userAgents
import re

#pylint: disable-msg=E1101, C0325, R0201, W0702, W0703

# A urllib2 wrapper that provides error handling and logging, as well as cookie management. It's a bit crude, but it works.

import gzip
import io

from threading import Lock
cookieWriteLock = Lock()

import iri2uri


class WebGetRobust:
	COOKIEFILE = 'cookies.lwp'				# the path and filename to save your cookies in
	cj = None
	cookielib = None
	opener = None



	errorOutCount = 2
	retryDelay = 1.5


	data = None

	# if test=true, no resources are actually fetched (for testing)
	# creds is a list of 3-tuples that gets inserted into the password manager.
	# it is structured [(top_level_url1, username1, password1), (top_level_url2, username2, password2)]
	def __init__(self, test=False, creds=None, logPath="Main.Web"):
		self.log = logging.getLogger(logPath)
		print("Webget init! Logpath = ", logPath)

		# Due to general internet people douchebaggyness, I've basically said to hell with it and decided to spoof a whole assortment of browsers
		# It should keep people from blocking this scraper *too* easily
		self.browserHeaders = userAgents.getUserAgent()

		self.testMode = test		# if we don't want to actually contact the remote server, you pass a string containing
									# pagecontent for testing purposes as test. It will get returned for any calls of getpage()

		self.data = urllib.parse.urlencode(self.browserHeaders)


		if creds:
			self.log.info("Have credentials, installing password manager into urllib handler.")
			passManager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			for url, username, password in creds:
				passManager.add_password(None, url, username, password)
			self.credHandler = urllib.request.HTTPBasicAuthHandler(passManager)
		else:
			self.credHandler = None

		self.loadCookies()

	def loadCookies(self):

		self.cj = http.cookiejar.LWPCookieJar()		# This is a subclass of FileCookieJar
												# that has useful load and save methods
		if self.cj is not None:
			if os.path.isfile(self.COOKIEFILE):
				try:
					self.cj.load(self.COOKIEFILE)
					self.log.info("Loading CookieJar")
				except:
					self.log.critical("Cookie file is corrupt/damaged?")

			if http.cookiejar is not None:
				self.log.info("Installing CookieJar")
				self.log.debug(self.cj)
				cookieHandler = urllib.request.HTTPCookieProcessor(self.cj)
				if self.credHandler:
					self.opener = urllib.request.build_opener(cookieHandler, self.credHandler)
				else:
					self.opener = urllib.request.build_opener(cookieHandler)
				#self.opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
				self.opener.addheaders = self.browserHeaders
				#urllib2.install_opener(self.opener)

		for cookie in self.cj:
			self.log.debug(cookie)
			#print cookie


	def chunkReport(self, bytesSoFar, totalSize):
		if totalSize:
			percent = float(bytesSoFar) / totalSize
			percent = round(percent * 100, 2)
			self.log.info("Downloaded %d of %d bytes (%0.2f%%)" % (bytesSoFar, totalSize, percent))
		else:
			self.log.info("Downloaded %d bytes" % (bytesSoFar))


	def chunkRead(self, response, chunkSize=2 ** 18, reportHook=None):
		contentLengthHeader = response.info().getheader('Content-Length')
		if contentLengthHeader:
			totalSize = contentLengthHeader.strip()
			totalSize = int(totalSize)
		else:
			totalSize = None
		bytesSoFar = 0
		pgContent = ""
		while 1:
			chunk = response.read(chunkSize)
			pgContent += chunk
			bytesSoFar += len(chunk)

			if not chunk:
				break

			if reportHook:
				reportHook(bytesSoFar, chunkSize, totalSize)

		return pgContent




		# postData expects a dict
		# addlHeaders also expects a dict
	def getpage(self, pgreq, addlHeaders = None, returnMultiple = False, callBack=None, postData=None, soup=False):

		# pgreq = fixurl(pgreq)
		# print pgreq
		# print type(pgreq)

		originalString = pgreq


		pgctnt = None
		pghandle = None

		loopctr = 0


		# Encode Unicode URL's properly
		pgreq = iri2uri.iri2uri(pgreq)

		try:
			# TODO: make this more sensible
			if addlHeaders != None and  postData != None:
				self.log.info("Making a post-request with additional headers!")
				pgreq = urllib.request.Request(pgreq, headers=addlHeaders, data=urllib.parse.urlencode(postData).encode("utf-8"))
			elif addlHeaders != None:
				pgreq = urllib.request.Request(pgreq, headers=addlHeaders)
			elif postData != None:
				self.log.info("Making a post request!")
				pgreq = urllib.request.Request(pgreq, data=urllib.parse.urlencode(postData).encode("utf-8"))

			else:
				pgreq = urllib.request.Request(pgreq)
		except:
			self.log.critical("Invalid header or url")
			raise

		errored = False
		lastErr = ""

		if not self.testMode:
			while 1:

				loopctr = loopctr + 1



				if loopctr > self.errorOutCount:
					self.log.error("Failed to retrieve Website : %s at %s All Attempts Exhausted", pgreq.get_full_url(), time.ctime(time.time()))
					pgctnt = None
					try:
						self.log.critical(("Critical Failure to retrieve page! %s at %s, attempt %s" % (pgreq.get_full_url(), time.ctime(time.time()), loopctr)))
						self.log.critical(("Error:", lastErr))
						self.log.critical("Exiting")
					except:
						self.log.critical("And the URL could not be printed due to an encoding error")
					break

				#print "execution", loopctr
				try:

					# print("request type = ", type(pgreq))
					pghandle = self.opener.open(pgreq)					# Get Webpage

				except urllib.error.HTTPError as e:								# Lotta logging
					self.log.warning("Error opening page: %s at %s On Attempt %s.", pgreq.get_full_url(), time.ctime(time.time()), loopctr)
					self.log.warning("Error Code: %s", e)

					#traceback.print_exc()
					lastErr = e
					try:

						self.log.warning("Original URL: %s", originalString)
						errored = True
					except:
						self.log.warning("And the URL could not be printed due to an encoding error")

					if e.code == 404:
						#print "Unrecoverable - Page not found. Breaking"
						self.log.critical("Unrecoverable - Page not found. Breaking")
						break

					time.sleep(self.retryDelay)

				except UnicodeEncodeError:
					self.log.critical("Unrecoverable Unicode issue retreiving page - %s", originalString)
					break

				except Exception:
					errored = True
					#traceback.print_exc()
					lastErr = sys.exc_info()
					self.log.warning("Retreival failed. Traceback:")
					self.log.warning(lastErr)
					self.log.warning(traceback.format_exc())

					self.log.warning("Error Retrieving Page! - Trying again - Waiting 2.5 seconds")

					try:
						self.log.critical("Error on page - %s" % originalString)
					except:
						self.log.critical("And the URL could not be printed due to an encoding error")

					time.sleep(self.retryDelay)


					continue

				if pghandle != None:
					try:

						self.log.info("Request for URL: %s succeeded at %s On Attempt %s. Recieving...", pgreq.get_full_url(), time.ctime(time.time()), loopctr)
						if callBack:
							pgctnt = self.chunkRead(pghandle, 2 ** 17, reportHook = callBack)
						else:
							pgctnt = pghandle.read()
						if pgctnt != None:

							self.log.info("URL fully retrieved.")

							preDecompSize = len(pgctnt)/1000.0

							encoded = pghandle.headers.get('Content-Encoding')
							#preLen = len(pgctnt)
							if encoded == 'deflate':
								compType = "deflate"

								pgctnt = zlib.decompress(pgctnt, -zlib.MAX_WBITS)

							elif encoded == 'gzip':
								compType = "gzip"

								buf = io.BytesIO(pgctnt)
								f = gzip.GzipFile(fileobj=buf)
								pgctnt = f.read()

							elif encoded == "sdch":
								raise ValueError("Wait, someone other then google actually supports SDCH compression?")

							else:
								compType = "none"

							decompSize = len(pgctnt)/1000.0
							# self.log.info("Page content type = %s", type(pgctnt))
							cType = pghandle.headers.get("Content-Type")
							self.log.info("Compression type = %s. Content Size compressed = %0.3fK. Decompressed = %0.3fK. File type: %s.", compType, preDecompSize, decompSize, cType)

							if "text/html" in cType:				# If this is a html/text page, we want to decode it using the local encoding

								if (";" in cType) and ("=" in cType): 		# the server is reporting an encoding. Now we use it to decode the

									dummy_docType, charset = cType.split(";")
									charset = charset.split("=")[-1]


								else:		# The server is not reporting an encoding in the headers.

									# this *should* probably be done using a parser.
									# However, it seems to be grossly overkill to shove the whole page (which can be quite large) through a parser just to pull out a tag that
									# should be right near the page beginning anyways.
									# As such, it's a regular expression for the moment

									# Regex is of bytes type, since we can't convert a string to unicode until we know the encoding the
									# bytes string is using, and we need the regex to get that encoding
									coding = re.search(rb"charset=[\'\"]?([a-zA-Z0-9\-]*)[\'\"]?", pgctnt, flags=re.IGNORECASE)

									cType = b""
									charset = None
									try:
										if coding:
											cType = coding.group(1)
											codecs.lookup(cType.decode("ascii"))
											charset = cType.decode("ascii")

									except LookupError:

										# I'm actually not sure what I was thinking when I wrote this if statement. I don't think it'll ever trigger.
										if (b";" in cType) and (b"=" in cType): 		# the server is reporting an encoding. Now we use it to decode the

											dummy_docType, charset = cType.split(b";")
											charset = charset.split(b"=")[-1]

									if not charset:
										self.log.warning("Could not find encoding information on page - Using default charset. Shit may break!")
										charset = "iso-8859-1"

								try:
									pgctnt = str(pgctnt, charset)

								except UnicodeDecodeError:
									self.log.error("Encoding Error! Stripping invalid chars.")
									pgctnt = pgctnt.decode('utf-8', errors='ignore')

								if soup:
									pgctnt = bs4.BeautifulSoup(pgctnt)
							elif "text/plain" in cType or "text/xml" in cType:
								pgctnt = bs4.UnicodeDammit(pgctnt).unicode_markup

							elif "text" in cType:
								self.log.critical("Unknown content type!")
								self.log.critical(cType)



							break


					except:
						print(("pghandle = ", pghandle))

						traceback.print_exc()
						self.log.error(sys.exc_info())
						self.log.error("Error Retrieving Page! - Transfer failed. Waiting %s seconds before retrying", self.retryDelay)

						try:
							self.log.critical("Critical Failure to retrieve page! %s at %s" % (pgreq.get_full_url(), time.ctime(time.time())))
							self.log.critical("Exiting")
						except:
							self.log.critical("And the URL could not be printed due to an encoding error")
						print()
						self.log.error(pghandle)
						time.sleep(self.retryDelay)






		if errored and pghandle != None:
			print(("Later attempt succeeded %s" % pgreq.get_full_url()))
			#print len(pgctnt)
		elif errored and pghandle == None:
			raise urllib.error.URLError("Failed to retreive page!")

		if returnMultiple:
			if self.testMode:
				raise ValueError("testing mode does not support multiple return values yet!")
			return pgctnt, pghandle
		else:
			if self.testMode:
				return self.testMode
			else:
				return pgctnt

	def syncCookiesFromFile(self):
		self.log.info("Synchronizing cookies with cookieFile.")
		if os.path.isfile(self.COOKIEFILE):
			self.cj.save("cookietemp.lwp")
			self.cj.load(self.COOKIEFILE)
			self.cj.load("cookietemp.lwp")
		# First, load any changed cookies so we don't overwrite them
		# However, we want to persist any cookies that we have that are more recent then the saved cookies, so we temporarily save
		# the cookies in memory to a temp-file, then load the cookiefile, and finally overwrite the loaded cookies with the ones from the
		# temp file

	def updateCookiesFromFile(self):
		if os.path.exists(self.COOKIEFILE):
			self.log.info("Synchronizing cookies with cookieFile.")
			self.cj.load(self.COOKIEFILE)
		# Update cookies from cookiefile

	def addCookie(self, inCookie):
		self.log.info("Updating cookie!")
		self.cj.set_cookie(inCookie)

	def addSeleniumCookie(self, cookieDict):
		# print cookieDict
		cookie = http.cookiejar.Cookie(
				version=0
				, name=cookieDict['name']
				, value=cookieDict['value']
				, port=None
				, port_specified=False
				, domain=cookieDict['domain']
				, domain_specified=True
				, domain_initial_dot=False
				, path=cookieDict['path']
				, path_specified=False
				, secure=cookieDict['secure']
				, expires=cookieDict['expiry']
				, discard=False
				, comment=None
				, comment_url=None
				, rest={"httponly":"%s" % cookieDict['httponly']}
				, rfc2109=False
			)

		self.cj.set_cookie(cookie)

	def initLogging(self):
			mainLogger = logging.getLogger("Main")			# Main logger
			mainLogger.setLevel(logging.DEBUG)

			ch = logging.StreamHandler(sys.stdout)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			ch.setFormatter(formatter)
			mainLogger.addHandler(ch)

	def saveCookies(self, halting=False):

		cookieWriteLock.acquire()
		# print("Have %d cookies before saving cookiejar" % len(self.cj))
		try:
			self.log.info("Trying to save cookies!")
			if self.cj is not None:							# If cookies were used

				self.syncCookiesFromFile()

				self.log.info("Have cookies to save")
				for cookie in self.cj:
					# print(cookie)
					# print(cookie.expires)

					if isinstance(cookie.expires, int) and cookie.expires > 30000000000:		# Clamp cookies that expire stupidly far in the future because people are assholes
						cookie.expires = 30000000000

				self.log.info("Calling save function")
				self.cj.save(self.COOKIEFILE)					# save the cookies again


				self.log.info("Cookies Saved")
			else:
				self.log.info("No cookies to save?")
		except Exception as e:
			print("Encountered an error on exit?")
			print("Exception = %s" % e)
		finally:
			cookieWriteLock.release()

		# print("Have %d cookies after saving cookiejar" % len(self.cj))
		if not halting:
			self.syncCookiesFromFile()
		# print "Have %d cookies after reloading cookiejar" % len(self.cj)

	def __del__(self):
		# print "WGH Destructor called!"
		self.saveCookies(halting=True)


def isList(obj):
	"""isList(obj) -> Returns true if obj is a Python list.

	This function does not return true if the object supplied
	is a UserList object.
	"""
	return type(obj) == list


def isTuple(obj):
	"isTuple(obj) -> Returns true if obj is a Python tuple."
	return type(obj) == tuple


class DummyLog:									# For testing WebGetRobust (mostly)
	logText = ""

	def __init__(self):
		pass

	def __repr__(self):
		return self.logText

	def write(self, string):
		self.logText = "%s\n%s" % (self.logText, string)

	def close(self):
		pass


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	print("Oh HAI")
	wg = WebGetRobust()

	content, handle = wg.getpage("http://www.lighttpd.net", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	content, handle = wg.getpage("http://www.example.org", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	content, handle = wg.getpage("https://www.google.com/images/srpr/logo11w.png", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	content, handle = wg.getpage("http://www.doujin-moe.us/ajax/newest.php", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
