from django.conf.urls import url
from django.contrib.auth import views as auth_views
# from django.urls import path
from . import views as core_views
from django.contrib import admin
# from django.urls import include, path

"""
urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^logout/$',auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^password/$', core_views.change_password, name='change_password'),
   	url(r'^email/$', core_views.change_email, name='change_email'),
]
"""
