#!/usr/bin/env python3
from os import environ
from flask import render_template
import datetime
import logging
import connexion
from connexion import NoContent

def get_summary(text):
    response = {
        "summary": "This is a dummy summary" 
    } 
    return response




logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('summarize.yaml')


# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')


# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
