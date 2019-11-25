"""cs251 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from core import views as core_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
"""
urlpatterns = [
	#path('', include('core.urls')),\
	url(r'^$', views.home, name='home'),
	path('qbank/', include('qbank.urls')),
    path('admin/', admin.site.urls),
]
"""



urlpatterns = [
	path('admin/', admin.site.urls),
    # url(r'^home$', core_views.home, name='home'),
    url(r'^$', RedirectView.as_view(url='/login/')),
    url(r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^logout/$',auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    # url(r'^signup/$', core_views.update_profile, name='signup'),
    url(r'^password/$', core_views.change_password, name='change_password'),
   	url(r'^email/$', core_views.change_email, name='change_email'),
   	path('qbank/', include('qbank.urls')),
   	
]
