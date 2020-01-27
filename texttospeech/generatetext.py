from io import StringIO
import string

import chardet
import six

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import io
import re
import textract
from pydub import AudioSegment
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="text-to-speech2020jan15-7335263c6ffb.json"


MAX_CHARACTER=4900

def decode(text):
        """Decode ``text`` using the `chardet
        <https://github.com/chardet/chardet>`_ package.
        """
        # only decode byte strings into unicode if it hasn't already
        # been done by a subclass
        if isinstance(text, six.text_type):
            return text

        # empty text? nothing to decode
        if not text:
            return u''

        # use chardet to automatically detect the encoding text
        result = chardet.detect(text)
        return text.decode(result['encoding'])



def process( byte_string, encoding):
        """Process ``filename`` and encode byte-string with ``encoding``. This
        method is called by :func:`textract.parsers.process` and wraps
        the :meth:`.BaseParser.extract` method in `a delicious unicode
        sandwich <http://nedbatchelder.com/text/unipain.html>`_.
        """
        # make a "unicode sandwich" to handle dealing with unknown
        # input byte strings and converting them to a predictable
        # output encoding
        # http://nedbatchelder.com/text/unipain/unipain.html#35
        #byte_string = self.extract(filename, **kwargs)
        unicode_string = decode(byte_string)
        return encode(unicode_string, encoding).decode("ascii")




##extract text using textract
def textExtract(ufile):
    #mp3 = request.FILES['up'] # or self.files['mp3'] in your form

    path = default_storage.save('temp/'+ufile.name, ContentFile(ufile.read()))
    text=textract.process((os.path.join(settings.MEDIA_ROOT, path)))
    default_storage.delete('temp/'+ufile.name)
    text=decode(text)
    
    return re.sub(r'[^\x20-\x7F]+',' ', text).strip()




def generateAudioPart(text,tts_params,TTS):
     # Instantiates a client
    client = texttospeech.TextToSpeechClient()

   # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    #print(synthesis_input)
    #print("################") 
    #print(text)
    #print("################") 

    # Build the voice request, select the language code ("en-US") 
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
    language_code=tts_params['languae'],
    name=tts_params['voice_name'],
    ssml_gender=tts_params['voice_gender'],) #texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
    pitch=tts_params['pitch'],
    speaking_rate=tts_params['speed'],
    effects_profile_id=[tts_params['audio_device_profile']],
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    #print(response)
    TTS.append(response.audio_content)
    print('page done:'+str(len(TTS)))
    # The response's audio_content is binary.
   

def generateAudio(text,path,tts_params):
    

   
    print(tts_params)
    TTS=[]
    r_text_start=0
    r_text_end=MAX_CHARACTER
    textLength=len(text)
    while r_text_start<textLength:

        while r_text_end<textLength and text[r_text_end] not in {' ','.',',','/'}:
            r_text_end=r_text_end+1
        if r_text_end>=textLength:
           text_part=text[r_text_start:]
        else:
           text_part=text[r_text_start:r_text_end]

        generateAudioPart(text_part,tts_params,TTS)
        r_text_start=r_text_end
        r_text_end=r_text_start+MAX_CHARACTER
        

        print("################") 
    output = AudioSegment.silent(duration=2000)

    for audio in TTS:
       s = io.BytesIO(audio) 
       output=output+AudioSegment.from_file(s)

   
    return output.export(format="mp3")
    


def processFile(ufile,tts_params):
    
    tts_params['voice_gender']=int(tts_params['voice_gender'])
    tts_params['speed']=float(tts_params['speed'])/100
    tts_params['pitch']=float(tts_params['pitch'])/10
    if tts_params['voice_gender']==0:
       tts_params['voice_gender']=texttospeech.enums.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED
    elif tts_params['voice_gender']==1:
       tts_params['voice_gender']=texttospeech.enums.SsmlVoiceGender.MALE
    elif tts_params['voice_gender']==2:
       tts_params['voice_gender']=texttospeech.enums.SsmlVoiceGender.FEMALE
    elif tts_params['voice_gender']==3:
       tts_params['voice_gender']=texttospeech.enums.SsmlVoiceGender.NEUTRAL
 
 
    text=textExtract(ufile)
    audio_path=settings.MEDIA_ROOT+'/'+ufile.name+'.mp3'
    audio_url=settings.BASE_URL+settings.MEDIA_URL+ufile.name+'.mp3'
    audio=generateAudio(text,audio_path,tts_params)

    return audio_url,text,audio,tts_params





#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.pdfpage import PDFPage
#from pdfminer.pdfparser import PDFParser
###pdf to text
#####method pdfminer
#def fromPDF(in_file):
 #       output_string = StringIO()
        #with open('', 'rb') as in_file:
  #      parser = PDFParser(in_file)
   #     doc = PDFDocument(parser)
    #    rsrcmgr = PDFResourceManager()
       # device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        #interpreter = PDFPageInterpreter(rsrcmgr, device)
        #for page in PDFPage.create_pages(doc):
         #   interpreter.process_page(page)

        #print(output_string.getvalue())



