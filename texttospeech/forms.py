from django import forms
class TTSForm(forms.Form):
    """Image upload form."""
    language= forms.CharField(required=True)
    voice_type=forms.CharField(required=True)
    voice_name=forms.CharField(required=True)
    audio_device_profile=forms.CharField(required=True)
    pitch=forms.CharField(required=True)
    speed=forms.CharField(required=True)
    upfile = forms.FileField()

