from django.db import models
import datetime
#from django.contrib.postgres.fields import ArrayField

class Qbank(models.Model):
    Name=models.TextField()
    Priv=models.TextField()
    Owner=models.TextField()
    No = models.IntegerField()
    def contains_keyword(self,kw1,kw2):
        flag = False
        for i in Qbank_Main.objects.all():
            if i.QbankNo == self:
                if kw2.lower().strip() in i.Content.lower():
                    flag = flag or True
        flag = flag and (kw1.lower().strip() in self.Name.lower())
        return flag 

class Qbank_Main(models.Model):
    Content = models.TextField()
    Difficulty = models.CharField(max_length = 6)
    Marks = models.IntegerField()
    Answer = models.TextField(null = True, blank = True,default='')
    tags = models.TextField(null=True , blank = True,default='')
    Chapter = models.TextField(default = "Chapter")
    Section = models.TextField(default = "Section")
    Owner = models.TextField()
    QbankNo = models.ForeignKey(Qbank, on_delete=models.CASCADE)
    IsModule = models.BooleanField()
    UploadNo = models.IntegerField(default=0)
    def filter(self,dic):
        """
        dic has following fields:
        keywords : list of keywords to be present in Content and answer
        difficulties : list of difficulties
        marks : pair of lower and upper bounds
        tags : list of tags
        owners : list of Owners
        """
        def sublist(lst1,lst2):
            for i in lst1:
                if i.lower().strip() not in lst2:
                    return False
            return True
        def intext(lst1,text):
            for i in lst1:
                if i.lower().strip() not in text.lower():
                    return False
            return True
        flag = True
        flag = flag and (intext(dic["keywords"],self.Content) or intext(dic["keywords"],self.Answer))
        flag = flag and (self.Difficulty in dic["difficulties"] or "All" in dic["difficulties"])
        if dic["marks"][0] is not None:
            flag = flag and self.Marks > dic["marks"][0] 
        if dic["marks"][1] is not None:
            flag = flag and self.Marks < dic["marks"][1]
        new_tags = [i.lower().strip() for i in self.tags.split(',')]
        flag = flag and (sublist(dic["tags"],new_tags) or "All" in dic["tags"])
        flag = flag and (self.Owner in dic["owners"] or "All" in dic["owners"])
        flag = flag and (self.Chapter in dic["chapter"] or "All" in dic["chapter"])
        flag = flag and (self.Section in dic["section"] or "All" in dic["section"])
        return flag

class Qbank_sub(models.Model):
	Parent = models.ForeignKey(Qbank_Main, on_delete=models.CASCADE)
	Content = models.TextField()
	Answer = models.TextField(null = True, blank = True)
	Marks = models.IntegerField(null = True, blank = True)

class Users(models.Model):
	UserName = models.TextField()
	Qbank = models.IntegerField()

class Qpaper(models.Model):
    Name= models.TextField()
    Questions= models.TextField() #comma sep id values
    Marks=models.IntegerField(default=0)
    Date = models.DateField(default=datetime.date.today)


# Create your models here.