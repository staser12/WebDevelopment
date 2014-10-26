import datetime
from django.db import models


class MyBlog(models.Model):
    title= models.CharField(max_length=30)
    content = models.TextField()
    pub_date=models.DateTimeField(default=datetime.datetime.now())
    version=models.IntegerField(default=0)



    @classmethod
    def getById(cls,id):
        return cls.objects.get(id=id)

    @classmethod
    def exists(cls,id):
        return len(cls.objects.filter(id=id))>0

    def __unicode__(self):
        return self.title

