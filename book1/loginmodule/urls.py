from django.urls import path, include
from django.conf.urls import url
from loginmodule.views import *



urlpatterns = [
	url(r'^register/$',signup),
	url(r'^login/$',login,name='login'),
	url(r'^logout/$',logout,name='logout'),
	
]