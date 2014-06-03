from django.db import models
from django.contrib.auth.models import User


class New(models.Model):
    date = models.DateField(auto_now=True)
    pic_url = models.CharField(max_length=100)
    new_type = models.CharField(max_length=20)
    name = models.TextField()
    info = models.TextField()
    lid = models.TextField()
    html = models.TextField()
    cviews = models.PositiveIntegerField( default=0 )
    ccomments = models.PositiveIntegerField( default=0 )
    authors = models.TextField()
    is_enabled = models.BooleanField( default = False )
    def __str__(self):
        return str(self.id) + ' ' + str(self.date)
    def __unicode__(self):
        return (str(self.id) + str(self.date))


import datetime

def get_records(n, mask, next):
    objects = New.objects.all().filter(is_enabled=True).order_by('-id')
    next=int(next)
    i = 0 if next == 0 else list(objects.values_list('id', flat=True)).index(next) + 1;
    j = 0
    selected_objects = []
    while(j < n and i < len(objects)):
        if((objects[i].new_type == mask or mask == "") and 
            objects[i].date <= datetime.date.today()):
            selected_objects.append(objects[i])
            j += 1
        i += 1
    return selected_objects


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
