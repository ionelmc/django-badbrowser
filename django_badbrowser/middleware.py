from django.conf import settings

from django_badbrowser import check_user_agent

class BrowserSupportDetection(object):
	def process_request(self, request):
		
		if not hasattr(settings, "BADBROWSER_REQUIREMENTS"):
			return None # no requirements have been setup
		
		if "HTTP_USER_AGENT" not in request.META:
			return None
		
		user_agent = request.META["HTTP_USER_AGENT"]
		
		if check_user_agent(user_agent, settings.BADBROWSER_REQUIREMENTS):
			return None # continue as normal
		else:
			return True # we need to return a response here
		
	
	


