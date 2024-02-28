from flask import Flask, render_template, request , url_for , send_file, Response , send_from_directory, Blueprint, redirect
import os
import json
import wave
import base64
import numpy as np
from utils import load_azure_data ,load_audio_file , check_file_availlability ,store_rating

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

filename = ''
ratings = ''


@app.route('/catch_filename', methods=['GET', 'POST'])
def catch_filename():
    global filename
    filename = request.form['filename']
    
    msg = check_file_availlability(filename)
    
    if msg =='Success':
        return redirect(url_for('audio_rater'))
    else:
        return render_template('not_exist.html',msg=msg)
    
    

@app.route('/audio_rater')

def audio_rater():
    
    wordToDisplay,counts = load_azure_data(filename)
    audioURL = load_audio_file(filename)
    return render_template('audio_rater.html',data = wordToDisplay,filename = f'{filename}-tblQuan_226_1',counts = counts,audioURL = audioURL)
    # return render_template('audio_rater_wave.html',data = wordToDisplay,filename = f'{filename}-tblQuan_226_1',counts = counts,audioURL = audioURL)


@app.route('/catch_rating', methods=['GET', 'POST'])
def catch_rating():
    global ratings
    ratings = request.get_json()
    
    store_rating(filename,ratings)

    return "Rating Saved For {}".format(filename)



if __name__ == '__main__':
    app.run(debug=True,port=7010)