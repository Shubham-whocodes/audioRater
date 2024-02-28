import os
import json
import wave
import numpy as np
from flask_cors import CORS 
from pydub import AudioSegment

def check_file_availlability(file):
    if os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/azure_json/{file}-tblQuan_226_1.json') and os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/audios/{file}-tblQuan_226_1.wav'):
        return 'Success'
    elif os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/azure_json/{file}-tblQuan_226_1.json') and not os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/audios/{file}-tblQuan_226_1.wav'):
        return 'No Audio File Found for --- {}'.format(file)
    elif not os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/azure_json/{file}-tblQuan_226_1.json') and os.path.exists(f'/home/shubham.kumar/svar_audio_rater/static/audios/{file}-tblQuan_226_1.wav'):
        return 'No Azure Timestamp File Found for --- {}'.format(file)
    else:
        return 'No Data found for CandidateID --- {}'.format(file)
    
    
def authenticateUser(username,password):
    with open('/home/shubham.kumar/svar_audio_rater/loginCreds.json','r') as fp:
        logins = json.load(fp)
    
    usernames = logins.keys()
    
    if username in usernames:
        if password == logins[username]:
            return 'Success'
        else:
            return 'Invalid Password'
    else:
        return 'Invalid Username'
    
    

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration_seconds = len(audio) / 1000
    return duration_seconds


def load_azure_data(file):
    with open(f'/home/shubham.kumar/svar_audio_rater/static/azure_json/{file}-tblQuan_226_1.json') as f:
        data = json.load(f)  
        
    audio_file = f'/home/shubham.kumar/svar_audio_rater/static/audios/{file}-tblQuan_226_1.wav'
        
    audio_duration = get_audio_duration(audio_file)
    total_words = len(data['words'])
    
    rateOfSpeech = total_words/audio_duration
    
    wordToDisplay = []
    
    longPauseDur = 0.0
    
    for i in range (0,len(data['words'])-1):
        diff = data['words'][i+1][1] - data['words'][i][3]
        t = 1000000 * 0.5
        if diff > t:
            longPauseDur+=diff
            wordToDisplay.append({"word": data['words'][i][0], "confidence": data['words'][i][4],'start':data['words'][i][1]/1000000,'duration':data['words'][i][2]/1000000,'end':data['words'][i][3]/1000000,'pause':'#'})
        else:
            wordToDisplay.append({"word": data['words'][i][0], "confidence": data['words'][i][4],'start':data['words'][i][1]/1000000,'duration':data['words'][i][2]/1000000,'end':data['words'][i][3]/1000000,'pause':''})
            
    wordToDisplay.append({"word": data['words'][-1][0], "confidence": data['words'][-1][4],'start':data['words'][-1][1]/1000000,'duration':data['words'][-1][2]/1000000,'end':data['words'][-1][3]/1000000,'pause':''})
    
    counts = {}
    c100=0
    c80=0
    c50=0
    c20=0
    wrong=0
    longPause  = 0 
    for item in wordToDisplay:
        if item['pause'] !='':
            longPause+=1
            
        if item['confidence'] == 1.0:
            c100+=1
        elif item['confidence'] < 1.0 and item['confidence'] >= 0.80:
            c80+=1
        elif item['confidence'] < 0.80 and item['confidence'] >= 0.50:
            c50+=1
        elif item['confidence'] < 0.50 and item['confidence'] >= 0.20:
            c20+=1
        else:
            wrong+=1
            
    counts.update({'c100':c100})
    counts.update({'c80':c80})
    counts.update({'c50':c50})
    counts.update({'c20':c20})
    counts.update({'wrong':wrong})
    counts.update({'longPause':longPause})
    
    longPauseDur/=1000000
    
    counts.update({'longPauseDur':round(longPauseDur,2)})
    counts.update({'rateOfSpeech':round(rateOfSpeech,2)})
    
    return wordToDisplay,counts


def load_audio_file(file):
    audio_file = f'/home/shubham.kumar/svar_audio_rater/static/audios/{file}-tblQuan_226_1.wav'
    with wave.open(audio_file, 'rb') as wav:
        audio_data = wav.readframes(wav.getnframes())

    return audio_data

def store_rating(filename,ratings):
    amcatID = filename.split('_')[0]
    sID = (filename.split('-')[0]).split('_')[1]
    outputDict = {}
    file =  f'{filename}-tblQuan_226_1'
    outputDict.update({'filename':file})
    outputDict.update({'CandidateID':amcatID})
    outputDict.update({'sID':sID})
    outputDict.update(ratings)
    
    with open(f'/home/shubham.kumar/svar_audio_rater/audio_ratings/{file}.json','w') as f:
        json.dump(outputDict,f,indent=2)    

    return "Rating Stored for {}".format(amcatID)

    