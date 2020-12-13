# test algorthim
# By Kevin Gonzaez (SimpleXTeam Leader)




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
      self.group1_hasStarted = False
      self.group2_hasStarted = False
      self.group1_percentage = 0
      self.group2_percentage = 0
      self.http_GET_Status = ""
      

   def getKeys(self):
      clearTerminal()
      return self.SavedVerseRequest

   def debugValidation(self):
      clearTerminal()
      run = 0
      length = 0
      for verse in self.testWrite:
         run += 1
         print "Group {}".format(run)
         for v in self.testWrite:
            length += len(v)
         print self.testWrite
         print "Group {}: {}".format(run, length)

   

         
   
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
                        # print innerList[loopIterator]
                        # PressEnterToContinue()


                        holdvalue.append(innerList[loopIterator])
                        self.testWrite.append(holdvalue)
                        holdvalue = []
                        holdvalue.append(innerList[loopIterator+1])

                     else:
                        print innerList[loopIterator]
                        # PressEnterToContinue()
                        holdvalue.extend((innerList[loopIterator], innerList[loopIterator+1]))
                        print "[+] Extending List"
                  except IndexError:
                     # IndexError: last element inside of list
                     print "[-] IndexError: {}".format(innerList[loopIterator])
                     holdvalue.append(innerList[loopIterator].encode("utf-8"))
            else:
                  tempVar = len(holdvalue)

                  #checksum holdvalue elements
                  for holdValueCounter in holdvalue:
                     # print "[+] Read -> {}".format(holdValueCounter)
                     holdvalue_counter += len(holdValueCounter)

                  print "[+] Total: {} | with checksum {}".format(getlength(), getlength()+holdvalue_counter)


                  # for iterator in range(tempVar):
                  if len(innerList[loopIterator]) + holdvalue_counter < 400:
                     print "[+] Value is still less than the maximum ({}, {}, {})".format(loopIterator, innerList[loopIterator], len(innerList[loopIterator])+holdvalue_counter)
                  # if len(innerList[loopIterator]) - len(holdvalue[iterator]) > 0:
                     # print "[+] Checking Difference: {} - {}".format(len(innerList[loopIterator]) - len(holdvalue[iterator]))
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
                     # print "[+] BreakingPoint {} ({})".format(len(holdvalue[iterator]) - len(innerList[loopIterator]), innerList[loopIterator])

                     y = 0
                     for vCheck in holdvalue:
                        y += len(vCheck)

                     
                     self.testWrite.append(holdvalue)

                     # print "[/\] Value is still less than the maximum ({}, {}, {})".format(loopIterator, innerList[loopIterator], len(innerList[loopIterator])+holdvalue_counter)
                     print "[+] Checked Element {} ({})".format(innerList[loopIterator], len(innerList[loopIterator]) + holdvalue_counter)
                     print "[+] Reached Max Value: {}".format(y)
                     print "[+] Sending List: {}".format(holdvalue)
                     print "[+] Sending Parameter -> {}".format(holdvalue)
                     print "[+] Send Write List: {}".format(self.testWrite)
                     # clearList(holdvalue)
                     
                     holdvalue = []
                     loopCounter += 1
                     continue

            self.group2_percentage = int((float(loopCounter)/int(innerListlength)*0.5*100))
            self.http_GET_Status = "Status: Formatting For Livestream ({}/{})".format(loopCounter+1, innerListlength)
            loopCounter += 1
            holdvalue_counter = 0
            # print holdvalue

      self.finish_parse_time = time.time() - start_parse_time
      self.testWrite.append(holdvalue)
      



   def appendDictionary(self, book, chapter, verses):
      # print "appendDictionary: {}".format(verses)
      self.SavedVerseRequest["{}:{}".format(book, chapter)] = verses
      # for saved in self.SavedVerseRequest:
      #    print "saved values: {}".format(saved)
      #    for s in self.SavedVerseRequest[saved]:
      #       print "\t saved list: {}".format(s)

   # def createFiles(self)

   # def clearCache(self, returnFiles=False):
   #    self.Files = os.listdir(os.getcwd())
   #    if returnFiles == False:
   #       for file in self.Files:
   #          if file != "main.py":
   #             if file != "test.py":
   #                if file != "web":
   #                   try:
   #                      os.remove(file)
   #                   except OSError:
   #                      pass
   #    else:
   #       return self.Files


   # def checkFilesExist(self, book, chapter, verse1, verse2):
   #    self.FilesDirectory = self.clearCache(returnFiles=True)
   #    if verse2 == None:
      

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
         self.jsonData.append("".join(verses))

      return self.jsonData

   def reset(self):
      self.group1_hasStarted = False
      self.group2_hasStarted = False
      self.group1_percentage = 0
      self.group2_percentage = 0
      self.book = ""
      self.verse1 = 0
      self.verse2 = 0
      # setUnicodeEncoding()   

   def getPercentage(self):
      self.percentage = 0
      if self.group1_hasStarted:
         if self.group2_hasStarted:
            self.percentage = self.group1_percentage + self.group2_percentage + 1
            if self.percentage != 100:
               return (self.percentage, self.http_GET_Status, "In-Progress")
            else:
               return (self.percentage, self.http_GET_Status, "Done")
         else:
            self.percentage = self.group1_percentage + 1
            if self.percentage != 100:
               return (self.percentage, self.http_GET_Status, "In-Progress")
            else:
               return (self.percentage, self.http_GET_Status, "Done")
            # return (self.percentage, self.http_GET_Status)
      else:
         return (self.percentage, self.http_GET_Status)


      # for verses in self.testWrite:
      #    fileName = book.replace(":", "")
      #    # if os.path.exists(str(os.getcwd) + fileName + ".txt") == False:
      #    #    os.makedirs("{}.txt".format(fileName))
      #    with open("{}.txt".format(fileName), "w+") as fileHandler:
      #       for verses in self.SavedVerseRequest[book]:
      #          fileHandler.write(verses)
   

   def checkSpecialCharacters(self, verse, initialFalseValue=False):
      # self.HtmlOutputReplace = ['(A)', '(B)']
      self.http_GET_Status = "Status: Fixing Verses / Unicode"
      self.x41SpecialCharacter = '(A)'
      self.x42SpecialCharacter = '(B)'
      self.x43SpecialCharacter = '(C)'
      self.x44SpecialCharacter = '(D)'
      self.x45SpecialCharacter = '(E)'

      self.x41BracketSpecialCharacter = '[a]'
      self.x42BracketSpecialCharacter = '[b]'
      self.x43BracketSpecialCharacter = '[c]'
      self.x44BracketSpecialCharacter = '[d]'


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

      if self.x43SpecialCharacter in verse:
         if self.x44SpecialCharacter in verse:
            # check for single spaces before replacing
            if verse[verse.find(self.x43SpecialCharacter)+3].isalpha():
               if verse[verse.find(self.x44SpecialCharacter)-1].isalpha():
                  verse = verse.replace(self.x43SpecialCharacter, '').replace(self.x44SpecialCharacter, ' ')
               else:
                  verse = verse.replace(self.x43SpecialCharacter, '').replace(self.x44SpecialCharacter, '')
            else:
               verse = verse.replace(self.x43SpecialCharacter, '').replace(self.x44SpecialCharacter, '')
            # return verse
         else:
            verse = verse.replace(self.x43SpecialCharacter, '')
            # return verse
      # else:

      # Fix (E) unicode bug
      if self.x45SpecialCharacter in verse:
         if verse[verse.find(self.x45SpecialCharacter)+3].isalpha():
            verse = verse.replace(self.x45SpecialCharacter, '')
         else:
            verse = verse.replace(self.x45SpecialCharacter, ' ')


      if self.x41BracketSpecialCharacter in verse:
         if self.x42BracketSpecialCharacter in verse:
            # check for single spaces before replacing
            if verse[verse.find(self.x42BracketSpecialCharacter)+3].isalpha():
               if self.pVerse[verse.find(self.x42BracketSpecialCharacter)-1].isalpha():
                  verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, ' ')
               else:
                  verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, '')
            else:
               verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, '')
            # return verse
         else:
            verse = verse.replace(self.x41BracketSpecialCharacter, '')
            # return verse
      # else:

      if self.x43BracketSpecialCharacter in verse:
         if self.x44BracketSpecialCharacter in verse:
            # check for single spaces before replacing
            if verse[verse.find(self.x43BracketSpecialCharacter)+3].isalpha():
               if verse[verse.find(self.x44BracketSpecialCharacter)-1].isalpha():
                  verse = verse.replace(self.x43BracketSpecialCharacter, '').replace(self.x44BracketSpecialCharacter, ' ')
               else:
                  verse = verse.replace(self.x43BracketSpecialCharacter, '').replace(self.x44BracketSpecialCharacter, '')
            else:
               verse = verse.replace(self.x43BracketSpecialCharacter, '').replace(self.x44BracketSpecialCharacter, '')
            # return verse
         else:
            verse = verse.replace(self.x43BracketSpecialCharacter, '')
            # return verse
      # else:
      

      # print "Verse: {}".format(verse)
      # remove spaces before start of string
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

      print "[+] Returning Verse: {}".format(verse)
      return verse


   def swapUnicodeToString(self, formatUnicode):
      tempVar = formatUnicode.replace("\xc2\xa0", " ")
      return tempVar



   def makeRequest(self, book, chapter, verse1, verse2, language):
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
                  self.group1_percentage = int((float(int(self.verse1))/int(self.verse1)*0.5*100))
                  # print "Single Verse: {}".format(self.returnedOutput)
      else:
         print "--------------- {} {}:{}-{} ----------------".format(book, chapter, self.verse1, self.verse2)
         self.requestCounter = self.verse1
         while self.requestCounter <= self.verse2+1:
            self.group1_percentage = int((float(self.requestCounter)/int(self.verse2)*0.5*100))
            self.http_GET_Status = "Status: Requesting Verses ({}/{})".format(self.requestCounter, self.verse2)
            multiRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest))
            # print "URL: https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest)
            if "No results found." in multiRequest.text:
               try:
                  raise ValueError
               except ValueError:
                  print "[-] Unable to fetch query for {} {}:{}".format(book, chapter, self.requestCounter)
                  exit(1)
            else:
               # print "Successful Request ({})".format(multiRequest.status_code)
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
                        # print "Without checkSpecialCharacters: {}".format(e)
                     else:
                        e = m.encode('utf-8')
                        holdVerses.append(e)
                        # print "NO CHECKS: {}".format(e)
                        # print e.decode('latin')
                     # print e
                     if self.requestCounter == 1:
                        self.returnedOutput = self.checkSpecialCharacters(e, True)
                     else:
                        self.returnedOutput = self.checkSpecialCharacters(e)
                     if language == "English":
                        holdVerses.append(self.returnedOutput)
                     # print "{} -> Length: {}".format(self.returnedOutput, len(self.returnedOutput))
               self.requestCounter += 1
               if self.requestCounter == self.verse2+1:
                  # print "Pass To Function: {}".format(holdVerses)
                  print "[+] HoldVerses: {}".format(holdVerses)


                  #debug
                  print "[DEBUG]: holdverses loop"
                  
                  for v in holdVerses:
                     holdVerses[holdVerses.index(v)] = holdVerses[holdVerses.index(v)].replace("\xc2\xa0", " ")

                  for vc in holdVerses:
                     # setUnicodeEncoding()
                     removeUnicodeEncoding()
                     print holdVerses[holdVerses.index(vc)]
                     
                     if "     " in holdVerses[holdVerses.index(vc)]:
                        if "   " in holdVerses[holdVerses.index(vc)]:
                           holdVerses[holdVerses.index(vc)] = holdVerses[holdVerses.index(vc)].replace("    ", "").replace("   ","")
                        else:
                           holdVerses[holdVerses.index(vc)] = holdVerses[holdVerses.index(vc)].replace("    ", "")
                     # else:
                     #    print "[DEBUG BREAKPOINT]: No Spaces Found"
                        # PressEnterToContinue()

                  setUnicodeEncoding()

                  self.appendDictionary(book, chapter, holdVerses)
                  self.ParseVerses(self.SavedVerseRequest, language)
                  clearTerminal()
                  break


clearTerminal()
setUnicodeEncoding()
# Livestream = LivestreamStudio()
# Livestream.clearCache()

# book = raw_input("Book: ")
# chapter = input("Chapter: ")
# verse1 = input("Verse 1: ")
# verse2 = input("Verse 2 (If None Enter 0): ")


# Livestream.makeRequest("Psalm", 51, 1, 19, "English")
# Livestream.makeRequest("Psalm", 51, 1, 19, "Spanish")

# Livestream.makeRequest("Hebrews", 12, 1, 11, "English")
# if verse2 == 0:
#    Livestream.makeRequest(book, chapter, verse1, None, "English")
# else:
#    Livestream.makeRequest(book, chapter, verse1, verse2, "Spanish")
# Livestream.makeRequest("2 Corintios", 7, 5, 8, "Spanish")
# Livestream.makeRequest("2 Corintios", 7, 5, 8, "English")
# Livestream.get()



# print "----------- PROGRAM DEBUG ------------"
# finish_time = time.time() - start_time
# print "Verse Parse Time: {} seconds".format(str(Livestream.finish_parse_time)[:4])
# print "Program Runtime: {} seconds".format(str(finish_time)[:4])
# print sys.argv
# PressEnterToContinue()




removeUnicodeEncoding()