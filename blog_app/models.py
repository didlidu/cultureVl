from django.db import models
from django.contrib.auth.models import User


class New(models.Model):
    date = models.DateField(auto_now=True)
    pic_url = models.CharField(max_length=100)
    #pic = models.ImageField(upload_to = './%Y/%m/%d')
    #pic = models.ImageField(verbose_name=u'Фото', upload_to='img', null=True, blank=True)
    new_type = models.PositiveIntegerField()
    name = models.TextField()
    lid = models.TextField()
    html = models.TextField()
    cviews = models.PositiveIntegerField( default=0 )
    ccomments = models.PositiveIntegerField( default=0 )
    authors = models.TextField()


def get_records(n, mask, next):
    objects = New.objects.all()
    if(mask == 0):
        return objects[ n * next : n * next + n ]
    i = n * next;
    j = 0
    selected_objects = []
    while(n + 10 and i < len(objects)):
        if(objects[i].new_type == mask):
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