import httpagentparser

from django.conf import settings
from django.core.urlresolvers import reverse

from django_badbrowser import check_user_agent

class BrowserSupportDetection(object):
	
	def _user_ignored_warning(self, request):
		"""Has the user forced ignoring the browser warning"""
		return "badbrowser_ignore" in request.COOKIES and request.COOKIES["badbrowser_ignore"]
	
	def process_request(self, request):
		self._clear_cookie = False
		
		if request.path.startswith(settings.MEDIA_URL):
			# no need to test media requests (which sometimes come via 
			# via django during development)
			return None
		
		if "HTTP_USER_AGENT" not in request.META:
			return None
		
		user_agent = request.META["HTTP_USER_AGENT"]
		parsed_user_agent = httpagentparser.detect(user_agent)
		
		# Set the browser information on the request object
		request.browser = parsed_user_agent
		
		if not hasattr(settings, "BADBROWSER_REQUIREMENTS"):
			return None # no requirements have been setup
		
		if request.path == reverse("django-badbrowser-ignore"):
			# Allow through any requests for the ignore page
			return None
		
		if check_user_agent(parsed_user_agent, settings.BADBROWSER_REQUIREMENTS):
			self._clear_cookie = True
			return None # continue as normal
		else:
			if self._user_ignored_warning(request):
				return None 
			
			from django_badbrowser.views import unsupported
			return unsupported(request)
	
	def process_response(self, request, response):
		if hasattr(self, "_clear_cookie") and self._clear_cookie:
			response.delete_cookie("badbrowser_ignore")
		return response
	


