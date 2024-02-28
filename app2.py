from flask import Flask, render_template, request , url_for , send_file, Response , send_from_directory, Blueprint, redirect
import os
import json
import wave
import base64
import numpy as np
from utils import load_azure_data ,load_audio_file , authenticateUser ,store_rating
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host = "192.168.59.24",
    user = "contentr",
    password = "12345678"
)
cursor = db.cursor()



@app.route('/')
def home():
    return render_template('login.html')

filename = '156634610055020_169'
ratings = ''


@app.route('/loginCreds', methods=['GET', 'POST'])
def catch_filename():
    global filename
    username = request.form['username']
    password = request.form['password']
    
    msg = authenticateUser(username,password)
    
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