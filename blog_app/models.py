from django.db import models

class New(models.Model):
    date = models.DateField(auto_now=True)
    pic_url = models.CharField(max_length=100)
    new_type = models.PositiveIntegerField()
    name = models.TextField()
    lid = models.TextField()
    html = models.TextField()