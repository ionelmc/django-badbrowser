import os

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest

from django_badbrowser.middleware import BrowserSupportDetection

class BrowserSupportDetectionTest(TestCase):
	
	def _get_ua_strings(self, file_):
		path = "%s/uastrings/%s.txt" % (os.path.dirname(__file__), file_)
		f = open(path, "r")
		lines = f.readlines()
		f.close()
		return lines
	
	def test_valid(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertTrue(bool(middleware.process_request(request)))
	
	def test_old_major_version(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/4.0.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertFalse(bool(middleware.process_request(request)))
	
	def test_old_minor_version(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.1.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.2.375.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertFalse(bool(middleware.process_request(request)))
	
	def test_equal_version(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.1.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.1.375.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertTrue(bool(middleware.process_request(request)))
	
	def test_user_agents_ie8_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "8"),)
		
		for ua in self._get_ua_strings("ie8"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie8_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "9"),)
		
		for ua in self._get_ua_strings("ie8"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie7_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "7"),)
		
		for ua in self._get_ua_strings("ie7"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie7_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "8"),)
		
		for ua in self._get_ua_strings("ie7"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie7b_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "7b"),) # "7a" or "7b" will allow beta, "7" will not
		
		for ua in self._get_ua_strings("ie7b"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie7b_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "7.0"),) # "7a" or "7b" will allow beta, "7" will not
		
		for ua in self._get_ua_strings("ie7b"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie6_1_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "6.1"),)
		
		for ua in self._get_ua_strings("ie6.1"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie6_1_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "6.2"),)
		
		for ua in self._get_ua_strings("ie6.1"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie6_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "6"),)
		
		for ua in self._get_ua_strings("ie6"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ie6_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("Microsoft Internet Explorer", "7"),)
		
		for ua in self._get_ua_strings("ie6"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_chrome_6_8_458_1_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("chromE", "6.0.458.1"),)
		
		for ua in self._get_ua_strings("chrome6.0.458.1"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_chrome_6_8_458_1_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("chromE", "6.0.458.2"),)
		
		for ua in self._get_ua_strings("chrome6.0.458.1"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ff_1_1_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("fireFox", "1.0"),)
		
		for ua in self._get_ua_strings("ff1.0"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ff_1_1_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("FIREFOX", "1.0.1"),)
		
		for ua in self._get_ua_strings("ff1.0"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ff_3_1_b_3_ok(self):
		settings.BADBROWSER_REQUIREMENTS = (("fireFox", "3.1 beta 3"),) # "3.1b3" will not work here
		
		for ua in self._get_ua_strings("ff3.1b3"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertTrue(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
	def test_user_agents_ff_3_1_b_3_bad(self):
		settings.BADBROWSER_REQUIREMENTS = (("FIREFOX", "3.1"),) # "3.1 beta 4" will not work here
		
		for ua in self._get_ua_strings("ff3.1b3"):
			request = HttpRequest()
			request.META["HTTP_USER_AGENT"] = ua
		
			middleware = BrowserSupportDetection()
			self.assertFalse(bool(middleware.process_request(request)), "Failed for UA '%s'" % ua)
	
























