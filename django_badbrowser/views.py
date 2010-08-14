from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings


def unsupported(request):
	
	if hasattr(settings, "BADBROWSER_SUGGEST"):
		suggest = settings.BADBROWSER_SUGGEST
	else:
		suggest = ("firefox",)
	
	context = {
		"next": request.path,
		"suggest": suggest,
		"MEDIA_URL": settings.MEDIA_URL,
	}
	
	return render_to_response("django_badbrowser/unsupported.html", context)

def ignore(request):
	response = HttpResponseRedirect(request.GET["next"] if "next" in request.GET else "/")
	response.set_cookie("badbrowser_ignore", True)
	return response
