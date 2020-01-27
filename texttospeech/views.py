from django.shortcuts import render
from django.shortcuts import redirect
from texttospeech.models import AudioFile
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from .forms import TTSForm
from django.core.files.base import ContentFile
import json
import requests
import io
from collections import OrderedDict

import os
import textract
from . import generatetext
from .serializers import  AudioFileSerializer


class GenerateAudio(APIView):

       
      def authenticated_request(self, request, *args, **kwargs):
        print(request.data) 
        print(request.FILES)
        
        tts_params={
           'languae':request.data.get('languae'),
           'voice_name':request.data.get('voice_name'),
           'voice_gender':request.data.get('voice_gender'),
           'audio_device_profile':request.data.get('audio_device_profile'),
           'speed':request.data.get('speed'),
           'pitch':request.data.get('pitch'),
        }
        


       
        
        ufile=request.FILES['upfile']

        audio_url,text,audio,tts_params=generatetext.processFile(ufile,tts_params)
        ##save the conversion data
        audio_file=AudioFile()
        audio_file.user=request.user
        
        audio_file.language=tts_params['languae']
        audio_file.voice_name=tts_params['voice_name']
        #audio_file.voice_type=tts_params['voice_type']
        audio_file.device_profile=tts_params['audio_device_profile']
        audio_file.pitch=tts_params['pitch']
        audio_file.speed=tts_params['speed']
        audio_file.name=ufile.name.split('.')[0]+'.mp3'
        audio_file.audio.save(ufile.name+'.mp3',audio,False)
        audio_file.source.save(ufile.name+'.txt',ContentFile(text),False)
        audio_file.save()
        
        
      
        #print(f.read())
        print('Audio content written to file "output.mp3"')
       

        return Response(data={'audio_url':audio_file.audio.url}, status=status.HTTP_200_OK)


     
      def post(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
           return Response(data={'login_url':webapi.settings.BASE_URL},status=status.HTTP_401_UNAUTHORIZED)
        else:
           return self.authenticated_request(request, *args, **kwargs)


class GetAudios(APIView):
      
     def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
           return Response(data={'error':'Not logged in.'},status=status.HTTP_401_UNAUTHORIZED)

        audios=AudioFile.objects.filter(user=request.user).order_by('-updated')

        print(audios)
        serialized_audios=AudioFileSerializer(audios,many=True)
        response=json.dumps(serialized_audios.data)
        print(response)
        return Response(data=response,status=status.HTTP_200_OK)

        



















