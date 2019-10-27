from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ini', views.upload_file, name = "ini"),
    path('a',views.add, name='add'),
]
