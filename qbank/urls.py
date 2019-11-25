from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ini', views.upload_file, name = "ini"),
    path('a',views.add, name='add'),
    path('ep',views.eform,name='eform'),
    path('first/',views.ltable,name='ltable'),
#    path('first/<str:sel>',views.ltable,name='ltable'),
    path('qpdet/<int:kid>',views.qpdet,name='qpdet'),
    path('det/<int:no>',views.detail,name='detail'),
    path('ed',views.edit,name='edit'),
   # path('first/<str:sel>',views.ltable,name='ltable')
    path('cvhelp/<str:no>',views.cvhelp, name='cvhelp'),
    path('qlist/<str:no>',views.qlist,name='qlist'),
    path('cv',views.cardv, name='cv'),
    path('mqp',views.make_qp, name='choose_frqp'),
    path('lv',views.lv,name='lv'),
    path('delhelp/<str:no>',views.delhelp,name='delhelp'),
    path('ctoini/<str:no>',views.ctoini,name='ctoini'),
    path('qpsave',views.qpsave,name='qpsave'),
    #path('first/<str:sel>',views.ltable,name='ltable')
]
