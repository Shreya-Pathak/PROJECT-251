from django.contrib import admin
from qbank.models import Qbank_Main
from qbank.models import Qbank_sub,Qpaper
# Register your models here.

admin.site.register(Qbank_Main)
admin.site.register(Qpaper)
admin.site.register(Qbank_sub)