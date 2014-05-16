from django.db import models

class New(models.Model):
    date = models.DateField(auto_now=True)
    pic_url = models.CharField(max_length=100)
    pic = models.ImageField(upload_to = './%Y/%m/%d')
    #pic = models.ImageField(verbose_name=u'Фото', upload_to='img', null=True, blank=True)
    new_type = models.PositiveIntegerField()
    name = models.TextField()
    lid = models.TextField()
    html = models.TextField()
    cviews = models.PositiveIntegerField( default=0 )
    ccomments = models.PositiveIntegerField( default=0 )