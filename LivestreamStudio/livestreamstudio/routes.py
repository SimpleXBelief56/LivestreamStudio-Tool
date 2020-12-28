from flask import render_template, url_for, redirect, flash, request, jsonify
from forms import RequestVerses
from livestreamstudio import app
from livestream import LivestreamStudio
import os
import time

Livestream = LivestreamStudio()

@app.route("/", methods=['GET'])
def home():
   return render_template('index.html')

@app.route("/parse", methods=['GET'])
def parse():
   # requestForm = RequestVerses()
   # Livestream = LivestreamStudio()
   # if requestForm.validate_on_submit:
   #    Livestream.makeRequest(requestForm.book.data, requestForm.chapter.dat, requestForm.verse1.data, request.verse2.data)
   #    Livestream.getData()
   #    return render_template('')      
   # else:
   return render_template('parse/index.html')

@app.route("/parse_data", methods=['GET'])
def parse_data():
   # Livestream.reset()
   book = request.args.get('book_field')
   chapter = request.args.get('chapter_field')
   verse1 = request.args.get('verse1_field')
   verse2 = request.args.get('verse2_field')
   language = request.args.get('language_field')
   Livestream.makeRequest(book, chapter, int(verse1), int(verse2), language)
   # Livestream.reset()
   # return jsonify(Livestream.getData())
   # print "[+] Returning {}".format(jsonify(Livestream.getData()))
   return jsonify(Livestream.getData())

@app.route("/features", methods=['GET'])
def features():
   return render_template('features/index.html')

@app.route("/getPercentage", methods=['GET'])
def passPercentage():
   return jsonify(Livestream.getPercentage())
   # return jsonify(12,'Status: Check Console')

@app.route("/getPercentagetest", methods=['GET'])
def passtestPercentage():
   return jsonify("1")

