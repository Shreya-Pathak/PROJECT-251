from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ini', views.upload_file, name = "ini"),
    path('a',views.add, name='add'),
    path('ep',views.eform,name='eform'),

    path('det',views.detail,name='detail'),
    path('ed',views.edit,name='edit'),
   # path('first/<str:sel>',views.ltable,name='ltable')

    path('first/<str:sel>',views.ltable,name='ltable')

]
