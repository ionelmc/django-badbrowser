from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def unsupported(request):
	return render_to_response("django_badbrowser/unsupported.html", { "next": request.path }, RequestContext(request))

def ignore(request):
	response = HttpResponseRedirect(request.GET["next"] if "next" in request.GET else "/")
	response.set_cookie("badbrowser_ignore", True)
	return response
