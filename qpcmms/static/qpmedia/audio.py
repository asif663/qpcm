# def playAudioFile(request):
#     fname="/home/chinna/Desktop/01 - Kajalu Chellivaa.mp3"
#     f = open(fname,"rb") 
#     response = HttpResponse()
#     response.write(f.read())
#     response['Content-Type'] ='audio/mp3'
#     response['Content-Length'] =os.path.getsize(fname )
#     return response

import pyttsx

engine = pyttsx.init()
engine.say("Pending")
engine.runAndWait()