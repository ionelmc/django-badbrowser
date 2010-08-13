import httpagentparser
from pkg_resources import parse_version

from django.conf import settings

class BrowserSupportDetection(object):
	def process_request(self, request):
		
		if not hasattr(settings, "BADBROWSER_REQUIREMENTS"):
			return None
		
		user_agent = request.META['HTTP_USER_AGENT']
		if not user_agent:
			return None
		
		parsed = httpagentparser.detect(user_agent)
		
		if "browser" not in parsed:
			return None
		
		if "name" not in parsed["browser"]:
			return None
		
		if "version" not in parsed["browser"]:
			return None
		
		user_browser = parsed["browser"]["name"].lower()
		user_browser_version = parsed["browser"]["version"]
		
		for browser, browser_version in settings.BADBROWSER_REQUIREMENTS:
			if user_browser == browser.lower():
				if cmp(parse_version(browser_version), parse_version(user_browser_version)) > 0:
					return None
		
		return True
	
	


