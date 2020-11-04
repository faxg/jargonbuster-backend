#!/usr/bin/env python3
from os import environ
import tempfile
import datetime
import logging

from flask import render_template
from flask import request
import connexion
from connexion import NoContent

from summarizer.lsa_summarizer import LsaSummarizer
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

import pdfminer.high_level


# Connexion request handling:
# https://connexion.readthedocs.io/en/latest/request.html

def generate_summary (data):
    #print (f"{request.get_data(as_text=True)}")
    inputText = data['text']
    summaryText = ""

    summarizer = LsaSummarizer()
    sw = stopwords.words('english')

    summarizer.stop_words = sw
    summaryText =summarizer(inputText, 3)


    response = {
        "summary": summaryText 
    } 
    return response


def post_summary():
    # see https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
    return generate_summary (request.json)





def post_extract():
    # 1. write temp file to disk
    f = request.files['file'] # uploaded file (via form / REST client)
    temp = tempfile.NamedTemporaryFile(prefix="jargonbuster_")
    extractedText = ""
    try:        
        f.save(temp.name)    
        # 2. use pdfminer to extract plain text
        # see https://pdfminersix.readthedocs.io/en/latest/reference/highlevel.html#api-extract-text
        extractedText = pdfminer.high_level.extract_text (temp.name, )
        # 3. TODO do some basic cleaning (e.g. linebreaks)
    finally:
        temp.close()    

    response = {
        "text": extractedText
    }


 
    return response




def post_analyze(body):
    data = request.json

    response = {
        "summary": "This is POST analyze: " + data['text']
    } 
    return response




def get_ir_token ():
    response = {
        "summary": "This is GET IR token" 
    } 
    return response




logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')


#
# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')





if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
