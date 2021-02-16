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
from langdetect import detect

start_time = time.time()
finish_parse_time = 0



testWrite = []
holdvalue = []
maxLength = 400

def clearTerminal():
   if platform.system() == "Windows":
      os.system("cls")
   else:
      os.system("clear")


def PressEnterToContinue():
   raw_input("Press Enter To Continue")
   pass


def setUnicodeEncoding():
   if platform.system() == "Windows":
      os.system("chcp 65001")

def removeUnicodeEncoding():
   if platform.system() == "Windows":
      os.system("chcp 437")


def write(vParamToWrite):
   for x in vParamToWrite:
      vHTMLReturn = " ".join(x)
      print vHTMLReturn
    

def getlength():
   count = 0
   for v in holdvalue:
      count += len(v)
   return count

# https://www.biblegateway.com/passage/?search=Exodo+3&version=RVR1960
#             ^^^^^^^^^^^                      ^^^^^ ^ ^^^^^^^^^^^^^^^
#                URL                           BOOK  Ch.  Version Query
#https://www.biblegateway.com/passage/?search=Exodo+3  %3A3-5   &version=RVR1960
#                                                      ^^^^^^
#                                                      Query 
#                                                      Verses

class LivestreamStudio:
   def __init__(self):
      if platform.system() == "Windows":
         os.system("cls")
      else:
         os.system("clear")
      self.Books = []
      self.LanguageKey = {"english":"ESV","spanish":"RVR1960"}
      self.FixedVersesNoHtml = []
      self.SavedVerseRequest = {}
      self.HoldValue = ""
      self.verseHolders = []
      self.error_callback = False
      self.group1_hasStarted = False
      self.group2_hasStarted = False
      self.group1_percentage = 0
      self.group2_percentage = 0
      self.http_GET_Status = ""
      

   def getKeys(self):
      clearTerminal()
      return self.SavedVerseRequest
   
   def ParseVerses(self, keyValues, language):
      self.group2_hasStarted = True
      start_parse_time = time.time()
      self.testWrite = []


      for x in keyValues:
         print "\n\n"
         holdvalue = []


         innerList = keyValues[x]
         innerListlength = len(innerList)
         holdvalue_counter = 0
         loopCounter = 0
         loopIterator = 0

         for loopIterator in range(innerListlength):
            print "-------- TEST CONDITION {} ({}) --------".format(loopCounter, loopIterator)
            print "[+] Checking if (holdvalue) is empty"

            if len(holdvalue) == 0:
                  print "[+] List has nothing"
                  try:
                     if len(innerList[loopIterator]) + len(innerList[loopIterator+1]) > 400:
                        holdvalue.append(innerList[loopIterator])
                        self.testWrite.append(holdvalue)
                        holdvalue = []
                        holdvalue.append(innerList[loopIterator+1])
                     else:
                        print innerList[loopIterator]
                        holdvalue.extend((innerList[loopIterator], innerList[loopIterator+1]))
                        print "[+] Extending List"
                  except IndexError:
                     # IndexError: last element inside of list
                     print "[-] IndexError: {}".format(innerList[loopIterator])
                     try:
                        holdvalue.append(innerList[loopIterator].encode("utf-8"))
                     except:
                        holdvalue.append(innerList[loopIterator])
            else:
                  tempVar = len(holdvalue)

                  #checksum holdvalue elements
                  for holdValueCounter in holdvalue:
                     holdvalue_counter += len(holdValueCounter)

                  print "[+] Total: {} | with checksum {}".format(getlength(), getlength()+holdvalue_counter)


                  if len(innerList[loopIterator]) + holdvalue_counter < 400:
                     print "[+] Value is still less than the maximum ({}, {}, {})".format(loopIterator, innerList[loopIterator], len(innerList[loopIterator])+holdvalue_counter)

                     print "[+] InnerList (keyvalues): {}".format(innerList)

                     # check if element already exists inside if the list
                     try:
                        if innerList[loopIterator+1] in holdvalue:
                           loopIterator += 2
                           loopCounter += 1
                           continue
                        else:
                           print "[+] Appending To List: {}".format(innerList[loopIterator+1])
                           holdvalue.append(innerList[loopIterator+1])
                     except IndexError:
                        holdvalue.append(innerList[loopIterator])


                  else:
                     y = 0
                     for vCheck in holdvalue:
                        y += len(vCheck)

                     self.testWrite.append(holdvalue)
                     print "[+] Checked Element {} ({})".format(innerList[loopIterator], len(innerList[loopIterator]) + holdvalue_counter)
                     print "[+] Reached Max Value: {}".format(y)
                     print "[+] Sending List: {}".format(holdvalue)
                     print "[+] Sending Parameter -> {}".format(holdvalue)
                     print "[+] Send Write List: {}".format(self.testWrite)
                     
                     holdvalue = []
                     loopCounter += 1
                     continue

            self.group2_percentage = int((float(loopCounter)/int(innerListlength)*0.5*100))
            self.http_GET_Status = "Status: Formatting For Livestream ({}/{})".format(loopCounter+1, innerListlength)
            loopCounter += 1
            holdvalue_counter = 0
            # print holdvalue

      self.finish_parse_time = time.time() - start_parse_time
      self.group2_percentage = int((float(loopCounter)/int(innerListlength)*0.5*100))
      if holdvalue != []:
         self.testWrite.append(holdvalue)
      



   def appendDictionary(self, book, chapter, verses):
      self.SavedVerseRequest["{}:{}".format(book, chapter)] = verses   

   def writeFiles(self):
      # Write lines to file
      self.formatVerseList = []
      print self.testWrite

      for verses in self.testWrite:
         self.formatVerseList.append("".join(verses))

      fileName = self.book.replace(":", "")

      with open("{}.txt".format(fileName), "w+") as fileHandler:
         for verses in self.formatVerseList:
            try:         
               fileHandler.writelines(verses + "\n\n")
            except TypeError:
               pass

   def getData(self):
      self.jsonData = []
      for verses in self.testWrite:
         self.jsonData.append(" ".join(verses))

      return self.jsonData

   def reset(self):
      self.group1_hasStarted = False
      self.group2_hasStarted = False
      self.group1_percentage = 0
      self.group2_percentage = 0
      self.book = ""
      self.verse1 = 0
      self.verse2 = 0  

   def getPercentage(self):
      self.percentage = 0
      if self.error_callback == True:
         self.reset()
         return (self.percentage, "404", "ERROR: Unable To Fetch Query")

      if self.group1_hasStarted:
         if self.group2_hasStarted:
            self.percentage = self.group1_percentage + self.group2_percentage
            if self.percentage != 100:
               return (self.percentage, self.http_GET_Status, "In-Progress")
            else:
               return (self.percentage, self.http_GET_Status, "Done")
         else:
            self.percentage = self.group1_percentage
            if self.percentage != 100:
               return (self.percentage, self.http_GET_Status, "In-Progress")
            else:
               return (self.percentage, self.http_GET_Status, "Done")
            # return (self.percentage, self.http_GET_Status)
      else:
         return (self.percentage, self.http_GET_Status)
   

   def checkSpecialCharacters(self, verse, initialFalseValue=False):
      self.http_GET_Status = "Status: Fixing Verses / Unicode"
      self.specialCharactersList = ['(A)','(B)','(C)','(D)','(E)','[a]','[b]','[c]','[d]']
      self.x41SpecialCharacter = '(A)'
      self.x42SpecialCharacter = '(B)'
      self.x43SpecialCharacter = '(C)'
      self.x44SpecialCharacter = '(D)'
      self.x45SpecialCharacter = '(E)'

      self.x41BracketSpecialCharacter = '[a]'
      self.x42BracketSpecialCharacter = '[b]'
      self.x43BracketSpecialCharacter = '[c]'
      self.x44BracketSpecialCharacter = '[d]'


      self.basics = [',','.','?',';']


      self.pVerse = verse

      # go through list
      for specialCharacter in self.specialCharactersList:
         if specialCharacter in self.pVerse:
            try:
               if self.pVerse[self.pVerse.find(specialCharacter)+3].isalpha():
                  if self.pVerse[self.pVerse.find(specialCharacter)-1].isalpha():
                     self.pVerse = self.pVerse.replace(specialCharacter, ' ')
                  else:
                     self.pVerse = self.pVerse.replace(specialCharacter, '')
               else:
                  self.pVerse = self.pVerse.replace(specialCharacter, '')
            except IndexError:
               if self.pVerse[self.pVerse.find(specialCharacter)-1].isalpha():
                  self.pVerse = self.pVerse.replace(specialCharacter, ' ')
               else:
                  self.pVerse = self.pVerse.replace(specialCharacter, '')
                  continue

      verse = self.pVerse


      if verse[0] == " ":
         verse = verse[1:]
         # print "Removed Spaces: {}".format(verse)

      if verse[0].isdigit() == True:
         if verse[1].isalpha() == True:
            # Format Correctly
            verse = verse.replace(verse[0], "{} ".format(verse[0]))
            # print "Final Format: {}".format(verse)

      if verse[0].isdigit() == True:
         if verse[1].isdigit() == True:
            if verse[2].isalpha() == True:
               verse = verse.replace(verse[:2], "{} ".format(verse[:2]))
            if verse[2].isdigit() == True:
               verse = verse.replace(verse[:3], "{} ".format(verse[:3]))

      if initialFalseValue == True:
         if verse[0].isdigit() == True:
            verse = verse.replace(verse[0], str(1))

      for basic in self.basics:
         if basic in verse:
            try:
               if verse[verse.find(basic)+1].isalpha():
                  verse = verse.replace(verse[verse.find(basic)], "{} ".format(verse[verse.find(basic)]))
            except IndexError:
               verse = verse.replace(verse[verse.find(basic)], "{} ".format(verse[verse.find(basic)]))

      print "[+] Returning Verse: {}".format(verse)
      return verse


   def swapUnicodeToString(self, formatUnicode):
      tempVar = formatUnicode.replace("\xc2\xa0", " ")
      return tempVar



   def makeRequest(self, book, chapter, verse1, verse2, language):
      self.SavedVerseRequest = {}
      self.group1_hasStarted = False
      self.group2_hasStarted = False
      self.group1_percentage = 0
      self.group2_percentage = 0
      self.book = ""
      self.verse1 = 0
      self.verse2 = 0
      self.error_callback = "No-Error"

      # AJAX Request Percentage Count
      self.group1_hasStarted = True

      self.book = book
      self.verse1 = verse1
      self.verse2 = verse2


      self.language = language
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
      if self.verse1 is None:
         print "--------------- {} {}:{} ----------------".format(book, chapter, self.verse1)
         singleRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.verse1, languageRequest))
         if "No results found." in singleRequest.text:
               try:
                  raise ValueError
               except ValueError:
                  print "[-] Unable to fetch query for {} {}:{}".format(book, chapter, self.verse1)
                  exit(1)
         else:
            HtmlParser = BeautifulSoup(singleRequest.content, 'lxml')
            commonElements = HtmlParser.find_all('div', {'class': 'passage-content'})
            for x in commonElements:
               c = x.findChildren('p')
               for v in c:
                  m = v.text
                  e = m.encode('ascii', 'ignore')
                  self.returnedOutput = self.checkSpecialCharacters(e)
                  self.group1_percentage = int((float(int(self.verse1))/int(self.verse1)*0.5*100))
      else:
         print "--------------- {} {}:{}-{} ----------------".format(book, chapter, self.verse1, self.verse2)
         self.requestCounter = self.verse1
         while self.requestCounter <= self.verse2+1:
            self.group1_percentage = int((float(self.requestCounter)/int(self.verse2)*0.5*100))
            self.http_GET_Status = "Status: Requesting Verses ({}/{})".format(self.requestCounter, self.verse2)
            multiRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest))
            if "No results found." in multiRequest.text:
               try:
                  raise ValueError
               except ValueError:
                  print "[-] Unable to fetch query for {} {}:{}".format(book, chapter, self.requestCounter)
                  self.error_callback = True
            else:
               HtmlParser = BeautifulSoup(multiRequest.content, 'lxml')
               commonElements = HtmlParser.find_all('div', {'class': 'passage-content'})
               for x in commonElements:
                  if x.find('div',{'class': 'poetry'}) is not None:
                     breakHtmlTag = x.find('br')
                     breakHtmlTag.string = u'\xa0'
                     print x.find("br")
                  c = x.findChildren('p')
                  for v in c:
                     m = v.text
                     if language == "English":
                        e = m.encode('ascii', 'ignore')
                     else:
                        e = m.encode('utf-8')
                        holdVerses.append(e)
                     if self.requestCounter == 1:
                        self.returnedOutput = self.checkSpecialCharacters(e, True)
                     else:
                        self.returnedOutput = self.checkSpecialCharacters(e)
                     if language == "English":
                        holdVerses.append(self.returnedOutput)
               self.requestCounter += 1
               if self.requestCounter == self.verse2+1:
                  print "[+] HoldVerses: {}".format(holdVerses)
                  print "[DEBUG]: holdverses loop"
                  
                  for v in holdVerses:
                     holdVerses[holdVerses.index(v)] = holdVerses[holdVerses.index(v)].replace("\xc2\xa0", " ")

                  for vc in holdVerses:
                     removeUnicodeEncoding()
                     print holdVerses[holdVerses.index(vc)]
                     
                     if "     " in holdVerses[holdVerses.index(vc)]:
                        if "   " in holdVerses[holdVerses.index(vc)]:
                           holdVerses[holdVerses.index(vc)] = holdVerses[holdVerses.index(vc)].replace("    ", "").replace("   ","")
                        else:
                           holdVerses[holdVerses.index(vc)] = holdVerses[holdVerses.index(vc)].replace("    ", "")

                  setUnicodeEncoding()

                  self.appendDictionary(book, chapter, holdVerses)
                  self.ParseVerses(self.SavedVerseRequest, language)
                  clearTerminal()
                  break


clearTerminal()
setUnicodeEncoding()
removeUnicodeEncoding()