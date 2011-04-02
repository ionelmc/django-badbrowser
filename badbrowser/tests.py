import os

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
from django.test.client import Client
from django.core.urlresolvers import reverse

from django_badbrowser import check_user_agent
from django_badbrowser.middleware import BrowserSupportDetection

class BrowserSupportDetectionTest(TestCase):
	
	def test_valid(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertEqual(middleware.process_request(request), None)
	
	def test_old_major_version(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/4.0.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		response = middleware.process_request(request)
		self.assertNotEqual(response, None)
		self.assertContains(response, "<!-- test data: unsupported browser -->")
	
	def test_old_major_version_ignore(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/4.0.375.126 Safari/533.4"
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		request.COOKIES["badbrowser_ignore"] = True
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		response = middleware.process_request(request)
		self.assertEqual(response, None)
	
	def test_no_user_agent(self):
		settings.BADBROWSER_REQUIREMENTS = (("Chrome", "5.0.175.126"),)
		
		request = HttpRequest()
		
		middleware = BrowserSupportDetection()
		self.assertEqual(middleware.process_request(request), None)
	
	def test_no_requirements_settings(self):
		ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/533.4"
		if hasattr(settings, "BADBROWSER_REQUIREMENTS"):
			del settings.BADBROWSER_REQUIREMENTS
		
		request = HttpRequest()
		request.META["HTTP_USER_AGENT"] = ua
		
		middleware = BrowserSupportDetection()
		self.assertEqual(middleware.process_request(request), None)
	

class IgnoreViewTest(TestCase):
	"""Testing for the ignore view"""
	
	def test_ignore(self):
		settings.BADBROWSER_REQUIREMENTS = (("Firefox", "3"),)
		
		c = Client()
		response = c.get(reverse("django-badbrowser-ignore"), HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/1.0")
		self.assertTrue("badbrowser_ignore" in c.cookies)
		self.assertTrue(bool(c.cookies["badbrowser_ignore"].value))
	
	def test_ignore_then_ok_browser(self):
		settings.BADBROWSER_REQUIREMENTS = (("Firefox", "3"),)
		
		c = Client()
		response = c.get(reverse("django-badbrowser-ignore"), HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/1.0")
		self.assertTrue("badbrowser_ignore" in c.cookies)
		self.assertTrue(bool(c.cookies["badbrowser_ignore"].value))
		
		response = c.get("/", HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/3.0")
		self.assertFalse(bool(c.cookies["badbrowser_ignore"].value))
	
	def test_ignore_then_ok_then_ignore(self):
		settings.BADBROWSER_REQUIREMENTS = (("Firefox", "3"),)
		
		c = Client()
		response = c.get(reverse("django-badbrowser-ignore"), HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/1.0")
		self.assertTrue("badbrowser_ignore" in c.cookies)
		self.assertTrue(bool(c.cookies["badbrowser_ignore"].value))
		
		response = c.get("/", HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/3.0")
		self.assertFalse(bool(c.cookies["badbrowser_ignore"].value))
		
		response = c.get(reverse("django-badbrowser-ignore"), HTTP_USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20050814 Firefox/1.0")
		self.assertTrue("badbrowser_ignore" in c.cookies)
		self.assertTrue(bool(c.cookies["badbrowser_ignore"].value))
	

class UnsupportedViewTest(TestCase):
	
	def test_simple(self):
		c = Client()
		response = c.get(reverse("django-badbrowser-unsupported"))
		self.assertContains(response, "<!-- test data: unsupported browser -->")
	

class CheckUserAgentTest(TestCase):
	
	def _get_ua_strings(self, file_):
		path = "%s/uastrings/%s.txt" % (os.path.dirname(__file__), file_)
		f = open(path, "r")
		lines = f.readlines()
		f.close()
		return lines
	
	def test_valid(self):
		user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/533.4"
		requirements = (("Chrome", "5.0.175.126"),)
		self.assertTrue(check_user_agent(user_agent, requirements))
	
	def test_valid_dict(self):
		user_agent = {'flavor': {'version': 'X 10_6_4', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '5.0.375.126', 'name': 'Chrome'}}
		requirements = (("Chrome", "5.0.175.126"),)
		self.assertTrue(check_user_agent(user_agent, requirements))
	
	def test_requirement_version_none(self):
		user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/533.4"
		requirements = (("Chrome", None),)
		self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_old_major_version_dict(self):
		user_agent = {'flavor': {'version': 'X 10_6_4', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '4.0.375.126', 'name': 'Chrome'}}
		requirements = (("Chrome", "5.0.175.126"),)
		self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_old_major_version(self):
		user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/4.0.375.126 Safari/533.4"
		requirements = (("Chrome", "5.0.175.126"),)
		self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_old_minor_version(self):
		user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.1.375.126 Safari/533.4"
		requirements = (("Chrome", "5.2.375.126"),)
		self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_equal_version(self):
		user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.1.375.126 Safari/533.4"
		requirements = (("Chrome", "5.1.375.126"),)
		self.assertTrue(check_user_agent(user_agent, requirements))
	
	def test_user_agents_ie8_ok(self):
		requirements = (("Microsoft Internet Explorer", "8"),)
		
		for user_agent in self._get_ua_strings("ie8"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie8_bad(self):
		requirements = (("Microsoft Internet Explorer", "9"),)
		
		for user_agent in self._get_ua_strings("ie8"):
			self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_user_agents_ie7_ok(self):
		requirements = (("Microsoft Internet Explorer", "7"),)
		
		for user_agent in self._get_ua_strings("ie7"):
			self.assertTrue(check_user_agent(user_agent, requirements))
	
	def test_user_agents_ie7_bad(self):
		requirements = (("Microsoft Internet Explorer", "8"),)
		
		for user_agent in self._get_ua_strings("ie7"):
			self.assertFalse(check_user_agent(user_agent, requirements))
	
	def test_user_agents_ie7b_ok(self):
		requirements = (("Microsoft Internet Explorer", "7b"),) # "7a" or "7b" will allow beta, "7" will not
		
		for user_agent in self._get_ua_strings("ie7b"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie7b_bad(self):
		requirements = (("Microsoft Internet Explorer", "7.0"),) # "7a" or "7b" will allow beta, "7" will not
		
		for user_agent in self._get_ua_strings("ie7b"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie6_1_ok(self):
		requirements = (("Microsoft Internet Explorer", "6.1"),)
		
		for user_agent in self._get_ua_strings("ie6.1"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie6_1_bad(self):
		requirements = (("Microsoft Internet Explorer", "6.2"),)
		
		for user_agent in self._get_ua_strings("ie6.1"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie6_ok(self):
		requirements = (("Microsoft Internet Explorer", "6"),)
		
		for user_agent in self._get_ua_strings("ie6"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ie6_bad(self):
		requirements = (("Microsoft Internet Explorer", "7"),)
		
		for user_agent in self._get_ua_strings("ie6"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_chrome_6_8_458_1_ok(self):
		requirements = (("chromE", "6.0.458.1"),)
		
		for user_agent in self._get_ua_strings("chrome6.0.458.1"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_chrome_6_8_458_1_bad(self):
		requirements = (("chromE", "6.0.458.2"),)
		
		for user_agent in self._get_ua_strings("chrome6.0.458.1"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ff_1_1_ok(self):
		requirements = (("fireFox", "1.0"),)
		
		for user_agent in self._get_ua_strings("ff1.0"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ff_1_1_bad(self):
		requirements = (("FIREFOX", "1.0.1"),)
		
		for user_agent in self._get_ua_strings("ff1.0"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ff_3_1_b_3_ok(self):
		requirements = (("fireFox", "3.1 beta 3"),) # "3.1b3" will not work here
		
		for user_agent in self._get_ua_strings("ff3.1b3"):
			self.assertTrue(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
	def test_user_agents_ff_3_1_b_3_bad(self):
		requirements = (("FIREFOX", "3.1"),) # "3.1 beta 4" will not work here
		
		for user_agent in self._get_ua_strings("ff3.1b3"):
			self.assertFalse(check_user_agent(user_agent, requirements), "Failed for ua '%s'" % user_agent)
	
























