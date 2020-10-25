# -*- coding: utf-8 -*-
# Livestream Verse Auto Parser
# By Kevin Gonzalez


import time
import random
import os
import platform
import sys
import requests
from bs4 import BeautifulSoup


# https://www.biblegateway.com/passage/?search=Exodo+3&version=RVR1960
#             ^^^^^^^^^^^                      ^^^^^ ^ ^^^^^^^^^^^^^^^
#                URL                           BOOK  Ch.  Version Query
#https://www.biblegateway.com/passage/?search=Exodo+3  %3A3-5   &version=RVR1960
#                                                      ^^^^^^
#                                                      Query 
#                                                      Verses

class LivestreamStudio:
   def __init__(self):
      self.Books = []
      self.LanguageKey = {"english":"ESV","spanish":"RVR1960"}
      self.FixedVersesNoHtml = []
      self.SavedVerseRequest = {}
      self.HoldValue = ""


   def appendDictionary(self, book, chapter, verses):
      print "appendDictionary: {}".format(verses)
      self.SavedVerseRequest["{}:{}".format(book, chapter)] = verses
      for saved in self.SavedVerseRequest:
         print "saved values: {}".format(saved)
         for s in self.SavedVerseRequest[saved]:
            print "\t saved list: {}".format(s)

   # def createFiles(self)

   def clearCache(self):
      self.Files = os.listdir(os.getcwd())
      for file in self.Files:
         if file != "main.py":
            os.remove(file)

   def writeFiles(self):
      # Write lines to file

      for book in self.SavedVerseRequest:
         fileName = book.replace(":", "")
         # if os.path.exists(str(os.getcwd) + fileName + ".txt") == False:
         #    os.makedirs("{}.txt".format(fileName))
         with open("{}.txt".format(fileName), "w+") as fileHandler:
            for verses in self.SavedVerseRequest[book]:
               fileHandler.write(verses)
   

   def checkSpecialCharacters(self, verse):
      # self.HtmlOutputReplace = ['(A)', '(B)']
      self.x41SpecialCharacter = '(A)'
      self.x42SpecialCharacter = '(B)'
      self.pVerse = verse

      if self.x41SpecialCharacter in self.pVerse:
         if self.x42SpecialCharacter in self.pVerse:
            # check for single spaces before replacing
            if self.pVerse[self.pVerse.find(self.x42SpecialCharacter)+3].isalpha():
               if self.pVerse[self.pVerse.find(self.x42SpecialCharacter)-1].isalpha():
                  verse = self.pVerse.replace(self.x41SpecialCharacter, '').replace(self.x42SpecialCharacter, ' ')
               else:
                  verse = self.pVerse.replace(self.x41SpecialCharacter, '').replace(self.x42SpecialCharacter, '')
            else:
               verse = self.pVerse.replace(self.x41SpecialCharacter, '').replace(self.x42SpecialCharacter, '')
            # return verse
         else:
            verse = self.pVerse.replace(self.x41SpecialCharacter, '')
            # return verse
      # else:
      

      print "Verse: {}".format(verse)
      # remove spaces before start of string
      if verse[0] == " ":
         verse = verse[1:]
         print "Removed Spaces: {}".format(verse)

      if verse[0].isdigit() == True:
         if verse[1].isalpha() == True:
            # Format Correctly
            verse = verse.replace(verse[0], "{} ".format(verse[0]))
            print "Final Format: {}".format(verse)
      return verse


   def makeRequest(self, book, chapter, verse1, verse2, language):
      # self.HtmlOutputReplace = ['(A)', '(B)']
      holdVerses = []
      if len(self.FixedVersesNoHtml) != 0:
         self.FixedVersesNoHtml = []

      if ' ' in book:
         book = book.replace(" ", "")

      try:
         languageRequest = self.LanguageKey[language.lower()]
      except:
         print "[-] Encountered an error trying to set language"
         exit(1)
      if verse2 is None:
         print "--------------- {} {}:{} ----------------".format(book, chapter, verse1)
         singleRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, verse1, languageRequest))
         if "No results found." in singleRequest.text:
               try:
                  raise ValueError
               except ValueError:
                  print "[-] Unable to fetch query for  {} {}:{}".format(book, chapter, self.requestCounter)
                  exit(1)
         else:
            # print "Successful Request ({})".format(singleRequest.status_code)
            # print "Retrieving class from common element"
            HtmlParser = BeautifulSoup(singleRequest.content, 'lxml')
            commonElements = HtmlParser.find_all('div', {'class': 'passage-content'})
            for x in commonElements:
               c = x.findChildren('p')
               for v in c:
                  m = v.text
                  e = m.encode('ascii', 'ignore')
                  self.returnedOutput = self.checkSpecialCharacters(e)
                  # print "Single Verse: {}".format(self.returnedOutput)
      else:
         print "--------------- {} {}:{}:{} ----------------".format(book, chapter, verse1, verse2)
         self.requestCounter = verse1
         while self.requestCounter <= verse2:
            multiRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest))
            print "URL: https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest)
            if "No results found." in multiRequest.text:
               try:
                  raise ValueError
               except ValueError:
                  print "[-] Unable to fetch query for  {} {}:{}".format(book, chapter, self.requestCounter)
                  exit(1)
            else:
               # print "Successful Request ({})".format(multiRequest.status_code)
               HtmlParser = BeautifulSoup(multiRequest.content, 'lxml')
               commonElements = HtmlParser.find_all('div', {'class': 'passage-content'})
               for x in commonElements:
                  c = x.findChildren('p')
                  for v in c:
                     m = v.text
                     if language == "English":
                        e = m.encode('ascii', 'ignore')
                        # print "Without checkSpecialCharacters: {}".format(e)
                     else:
                        e = m.encode('utf-8')
                        holdVerses.append(e)
                        # print "NO CHECKS: {}".format(e)
                        # print e.decode('latin')
                     # print e
                     self.returnedOutput = self.checkSpecialCharacters(e)
                     if language == "English":
                        holdVerses.append(self.returnedOutput)
                     # print "{} -> Length: {}".format(self.returnedOutput, len(self.returnedOutput))
               self.requestCounter += 1
               if self.requestCounter == verse2:
                  # print "Pass To Function: {}".format(holdVerses)
                  self.appendDictionary(book, chapter, holdVerses)
                  break


Livestream = LivestreamStudio()
Livestream.clearCache()
Livestream.makeRequest("Exodo", 3, 3, 5, "English")
Livestream.makeRequest("Exodo", 4, 1, 3, "English")
Livestream.makeRequest("2 Corintios", 7, 5, 8, "Spanish")
Livestream.makeRequest("2 Corintios", 7, 5, 8, "English")
Livestream.writeFiles()


# 2 Corintios 7

