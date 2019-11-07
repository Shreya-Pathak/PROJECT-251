from django.db import models
#from django.contrib.postgres.fields import ArrayField

class Qbank_Main(models.Model):
    Content = models.TextField()
    Difficulty = models.CharField(max_length = 6)
    Marks = models.IntegerField()
    Answer = models.TextField(null = True, blank = True,default='')
    tags = models.TextField(null=True , blank = True,default='')
    Chapter = models.TextField(default = "Chapter")
    Section = models.TextField(default = "Section")
    Owner = models.TextField()
    QbankNo = models.IntegerField()
    IsModule = models.BooleanField()
    UploadNo = models.IntegerField(default=0)

class Qbank_sub(models.Model):
	Parent = models.ForeignKey(Qbank_Main, on_delete=models.CASCADE)
	Content = models.TextField()
	Answer = models.TextField(null = True, blank = True)
	Marks = models.IntegerField(null = True, blank = True)

class Users(models.Model):
	UserName = models.TextField()
	Qbank = models.IntegerField()



# Create your models here.