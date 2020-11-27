#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import tempfile
import datetime
import logging
import requests
from pprint import pprint

from flask import Flask, redirect, render_template, request, jsonify
import connexion
from connexion import NoContent

from summarizer2 import summarizer 



import pdfminer.high_level
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


import re
from cleantext import clean


# load the .env file. 
# Make sure you create it and add the right keys etc. to run this locally.
# For cloud runtime, we store the secrets by other means ( make sure to update them as well)
load_dotenv()



# Connexion request handling:
# https://connexion.readthedocs.io/en/latest/request.html

def generate_summary (data: dict):
    #print (f"{request.get_data(as_text=True)}")
    inputText = data.get('text', '')

    method = data.get('method','lexrank')
    language = data.get('language',  'english')
    num_sentences = data.get ('num_sentences', 3)

    summaryText = ""
    print ("======= Start Summary creation ========== ")
    summaryText = summarizer.createSummary (inputText,language = language,num_sentences= num_sentences,method = method)
    #print (summaryText)
    print ("======= End Summary creation ========== ")
    
    summaryHTML = f'' 

    for x in range(len(summaryText)): 
	    summaryHTML = f'{summaryHTML} <li>{summaryText[x]}</li>' 
    summaryHTML = f'<ul>{summaryHTML}</ul>' 



    response = {
        "summary": summaryText,
        "html": summaryHTML
    } 
    return response


def post_summary():
    # see https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
    return generate_summary (request.json)


def get_definition ():
    apiKey = os.environ.get('MW_API_KEY')
    term = request.args['term']
    try:
        url = f"https://www.dictionaryapi.com/api/v3/references/medical/json/{term}?key={apiKey}"

        resp = requests.get (url)
        jsonResp = resp.json()

        # For now we only extract the first form and give the short descriptions
        fl = jsonResp[0]['fl']
        definitions = jsonResp[0]['shortdef']
        response = jsonify (term = term, fl = fl, definitions = definitions)

        return response
    except Exception as e:
        message = 'Error querying the MW dictionary: ' + resp.text
        print (message, e)
        return jsonify(error = message)


    




def post_extract():
    # 1. write temp file to disk
    f = request.files['file'] # uploaded file (via form / REST client)
    temp = tempfile.NamedTemporaryFile(prefix="jargonbuster_", delete=False)
    extractedText = ""
    info = ""
    try:        
        f.save (temp)    
        # 2. use pdfminer to extract plain text
        # see https://pdfminersix.readthedocs.io/en/latest/reference/highlevel.html#api-extract-text
        parser = PDFParser(temp)
        doc = PDFDocument(parser)
        info  = { key: val.decode() for key, val in doc.info[0].items() }
        print (info)
        temp.close()
        extractedText = pdfminer.high_level.extract_text (temp.name)
        # 3. do some basic cleaning (e.g. linebreaks)
        extractedText= clean (extractedText,
            no_line_breaks=True,
            lang="en")
        # remove remains from word breaks (like "re- miniscence")
        extractedText= re.sub(r'([a-z])\- ([a-z])', r'\1\2', extractedText)
        extractedText= re.sub(r'\.\d+\s+([a-z])+', r'\1', extractedText)
        
    finally:
        temp.close()
        os.unlink(temp.name)

    response = jsonify (text = extractedText, info= info)


 
    return response




def post_analyze():
    data = request.json
    
    fulltext = "".join (data['summary'])

    endpoint = os.environ.get('TA_ENDPOINT')

    # curl -X POST 'http://<serverURL>:5000/text/analytics/v3.2-preview.1/entities/health' --header 'Content-Type: application/json' --header 'accept: application/json' --data-binary @example.json


    try:
        url = f"{endpoint}/text/analytics/v3.2-preview.1/entities/health"
        documents = { "documents": [
            {"language": "en",
            "id": "1",
            "text": fulltext
            }]
        }
        #payload = jsonify(documents)
        #print (payload)

        resp = requests.post (url, 
            headers = {},
            json=documents)
        print (resp.text)

        if (resp.ok):
            print ("OK: ")
            raw = resp.json()['documents'][0]
            #category = Diagnosis
            diagnosis = next((sub for sub in raw['entities'] if sub['category'] == 'Diagnosis'), None) 
            # category=ExaminationName
            examinations = next((sub for sub in raw['entities'] if sub['category'] == 'ExaminationName'), None)
            # catgeory=TreatmentName
            treatments = next((sub for sub in raw['entities'] if sub['category'] == 'TreatmentName'), None)

            #jsonResp['entities']

            jsonResp = jsonify (diagnosis, examinations, treatments)

        else:
            #print (resp.status_code, resp.reason)
            jsonResp = jsonify (error = resp.reason)

        return jsonResp
    except Exception as e:
        message = f"Error calling Text Analytics for health: {str(e)}"  
        return jsonify(error = message)




#
# Get the Immersive Reader token.
#
def get_ir_token ():
    try:
        headers = { 'content-type': 'application/x-www-form-urlencoded' }
        data = {
            'client_id': str(os.environ.get('CLIENT_ID')),
            'client_secret': str(os.environ.get('CLIENT_SECRET')),
            'resource': 'https://cognitiveservices.azure.com/',
            'grant_type': 'client_credentials'
        }
        print (data)

        resp = requests.post('https://login.windows.net/' + str(os.environ.get('TENANT_ID')) + '/oauth2/token', data=data, headers=headers)
        jsonResp = resp.json()
        
        if ('access_token' not in jsonResp):
            print(jsonResp)
            raise Exception('AAD Authentication error')

        token = jsonResp['access_token']
        subdomain = str(os.environ.get('SUBDOMAIN'))

        return jsonify(token = token, subdomain = subdomain)
    except Exception as e:
        message = 'Unable to acquire Azure AD token. Check the debugger for more information.'
        print(message, e)
        return jsonify(error = message)




logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')


#
# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reader')
def reader():
    return render_template('reader.html')




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
