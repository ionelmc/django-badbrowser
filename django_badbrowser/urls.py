from django.conf.urls.defaults import *

from django_badbrowser.views import ignore

urlpatterns = patterns("",
	url(r"^ignore/$", ignore, name="django-badbrowser-ignore"),
)
