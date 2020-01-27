from django.urls import path,re_path
from django.conf.urls import include,url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views
urlpatterns = [
       # URLs that do not require a session or valid token
    path('',login_required(TemplateView.as_view(template_name="tts.html"))),
    path('texttospeech/', login_required(views.GenerateAudio.as_view()),name='texttospeech'),
    path('getaudios/', login_required(views.GetAudios.as_view()),name='get_audios'),
    

]

