"""sharathapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import *
from django.contrib import admin
from django import urls
from django.conf import settings


urlpatterns = [
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('accounts.urls')),
    url(r'^api/', include('expenses.urls')),
]


# only show the admin if the SHOW_ADMIN env variable is set to True
SHOW_ADMIN = True
if 'SHOW_ADMIN' in os.environ:
    SHOW_ADMIN = os.environ['SHOW_ADMIN']

if (SHOW_ADMIN is not None) and SHOW_ADMIN:
    urlpatterns += (
        url(r'^admin/', admin.site.urls),
    )
# import debug_toolbar
# urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns
