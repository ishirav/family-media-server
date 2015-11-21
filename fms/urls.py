"""fms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from fms.main.views import *


urlpatterns = [
    url(r'^admin/',           include(admin.site.urls)),
    url(r'^root/',            directory_view),
    url(r'^refresh/',         refresh_view),
    url(r'^cut_or_copy/$',    cut_or_copy_view, name='cut_or_copy'),
    url(r'^paste/',           paste_view, name='paste'),
    url(r'^delete/$',         delete_view, name='delete'),
    url(r'^new_folder/',      new_folder_view, name='new_folder'),
    url(r'^$',                home_view),
    url(r'^accounts/login/',  auth_views.login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/', auth_views.logout_then_login, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
