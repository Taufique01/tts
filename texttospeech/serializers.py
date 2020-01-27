from rest_framework import serializers
from django import forms
from texttospeech.models import AudioFile
from django.db.models import Count
from django.db.models.aggregates import Max
from django.contrib.auth.models import User


class AudioFileSerializer(serializers.ModelSerializer):

      url = serializers.SerializerMethodField('get_audio_url')


      class Meta:
          model = AudioFile
          fields = ('id','language','voice_type','voice_name','device_profile','speed','pitch','name','url')

      def get_audio_url(self, audio_file):
       
          return audio_file.audio.url
       

