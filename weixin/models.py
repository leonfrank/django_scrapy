from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.
'''
class Keyword(models.Model):
    name = models.CharField(max_length = 100)
'''

@python_2_unicode_compatible
class CompResult(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length = 100)
    created_time = models.DateTimeField()
    #description = models.TextField()
    #keywords = models.ManyToManyField(Keyword,blank = True)
    title_score = models.IntegerField()
    wx_link = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_time']
