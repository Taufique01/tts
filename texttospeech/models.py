
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models import Count
from django.db.models.aggregates import Max
# Create your models here.

# Create your models here.
class AudioFile(models.Model):
    user = models.ForeignKey(
        User,
        related_name='audio_file',
        null=False, blank=False, on_delete=models.CASCADE
    )
    language = models.CharField(max_length=100,null=False)
    name=models.CharField(max_length=100,null=False,default='unknown')
    voice_type=models.CharField(max_length=100,null=True,default='wavenet')
    voice_name=models.CharField(max_length=100,null=False)
    device_profile=models.CharField(max_length=100,null=False)
    speed=models.FloatField(null=False,default=1.0)
    pitch=models.FloatField(null=False,default=0)
    audio = models.FileField( upload_to = 'audios/%Y/%m/%d/', blank=False, null=False)
    source = models.FileField( upload_to = 'images/%Y/%m/%d', blank=False, null=False)
    updated = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
       
       self.updated=timezone.now()
       return super(AudioFile, self).save(*args, **kwargs)

    def __str__(self):
      return self.source.name+ ' ' + self.user.email

