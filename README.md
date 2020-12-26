# LivestreamStudio-Tool
Parse bible verses for Vimeo Livestream with this easy-to-use tool. With one click of a button, your ready to copy and paste the verses you need and live stream in no time.

# LivestreamStudio-Tool (Dependencies)
* Python 2.7
  * Flask
  * flask_bcrypt
  * langdetect
  
# How it works?

We utilize [BibleGateway](https://www.biblegateway.com/) to get the verses that we need for that day. Then we request those verses by url query method. For example

### Single Verse Request
```
https://www.biblegateway.com/passage/?search=Exodo+3&version=RVR1960
             ^^^^^^^^^^^                     ^^^^^ ^ ^^^^^^^^^^^^^^^
                URL                          BOOK  Ch.  Version Query

```

### Multi Verse Request
```
https://www.biblegateway.com/passage/?search=Exodo+3  %3A3-5   &version=RVR1960
                                                      ^^^^^^
                                                      Query 
                                                      Verses

```

With this method we do not need to specify the language cause the language is determine by the version query:
```
version=RVR1960
        ^^^^^^^ 

```
And we only utilize two versions which are RVR1960 and ESV

***

After we get a successful 200 - OK Response from the website, we can then get the text from the html that we recieved from the response. For this we use the request module to fulfill our request like so:

### Single Verse Request
```python

singleRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.verse1, languageRequest))

```

### Multi Verse Request
```python

multiRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest))

```

The reason why both line of code looks the same is because instead of requesting all the verses at once for the multi verse request, we use a while loop to count from the first verse to the last verse. The other reason why we do this is because each verse has a different class name that we need in order to parse. For example one verse in line 2 might contain
```html
<span id="en-ESV-15901" class="text Ps-119-2">
```
And another one
```html
<span id="en-ESV-15902" class="text Ps-119-3">
```
So, to make it more simpler and for better performance, we use a while loop to keep a count from the first verse all the way to the last verse. For example: 
```python
self.requestCounter = self.verse1 # First Verse
while self.requestCounter <= self.verse2+1:
```
And then while that while-loop runs, we request each time we loop using that single line url query method, like so:
```python

multiRequest = requests.get("https://www.biblegateway.com/passage/?search={}+{}%3A{}&version={}".format(book, chapter, self.requestCounter, languageRequest))

```
The **book**, **chapter**, **self.verse1**, **self.verse2**, and **languageRequest** variables, is fullfilled by the parameters for the function which is where all that code requesting is at:
```python
def makeRequest(self, book, chapter, verse1, verse2, language)
```
So, for example, if we want to request Psalm 119:10-50 in English, then we will call that function like so:
```python
def makeRequest("Psalm", 119, 10, 50, "English")
```
***
Once we got our verses, we run the html code through the BeautifulSoup Module in order to parse the text:
```python
HtmlParser = BeautifulSoup(multiRequest.content, 'lxml')
```
Then we find the verse, by finding a div with class name passage-content:
```python
commonElements = HtmlParser.find_all('div', {'class': 'passage-content'})
```
After we have got the specific html code that we need, we need to find the actual child-html code that contains the actual text. For this we iterate over the parent element, and proceed towards the child element. The only issue with this is that some chapters contain poetry format, which means text like this:
```
You have commanded your precepts
    to be kept diligently.
```
Gets translated to this
```
You have commanded your preceptsto be kept diligently.
```
The reason for this is the break-tag inserted in between, and when we use BeautifulSoup in order to parse the HTML, that tag is ignored except for the non-breaking space, which is not ignored. In order to prevent this we need to replace the tag with the special unicode character for the **&nbsp** set by BeautifulSoup which is **\xa0**. That way when we proceed to replace the &nbsp, we can replace it with a space for parsing and formatting:
```python
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
```
After we went through and checked for <br> and **&nbsp**, we then check for special type of character found within the text itself, adn the reason why its special is because those special characters are actual links, but instead they are single characters with square-brackets around them like so
```
[a], [b], [c], [d], [e]
```
These characters are unneseccary, so we remove them inside the **checkSpecialCharacters**
```python
 def checkSpecialCharacters(self, verse, initialFalseValue=False):
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
         else:
            verse = self.pVerse.replace(self.x41SpecialCharacter, '')

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
         else:
            verse = verse.replace(self.x43SpecialCharacter, '')

      # Fix (E) unicode bug
      if self.x45SpecialCharacter in verse:
         if verse[verse.find(self.x45SpecialCharacter)+3].isalpha():
            verse = verse.replace(self.x45SpecialCharacter, '')
         else:
            verse = verse.replace(self.x45SpecialCharacter, ' ')


      if self.x41BracketSpecialCharacter in verse:
         if self.x42BracketSpecialCharacter in verse:
            if verse[verse.find(self.x42BracketSpecialCharacter)+3].isalpha():
               if self.pVerse[verse.find(self.x42BracketSpecialCharacter)-1].isalpha():
                  verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, ' ')
               else:
                  verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, '')
            else:
               verse = verse.replace(self.x41BracketSpecialCharacter, '').replace(self.x42BracketSpecialCharacter, '')
         else:
            verse = verse.replace(self.x41BracketSpecialCharacter, '')

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
         else:
            verse = verse.replace(self.x43BracketSpecialCharacter, '')

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
```
***
After every verse has been requested and all special characters have been removed, we then move into the formatting stage, where we seperate by 400 characters. Livestream Studio 
only supports up to 400 characters per row in the data table. Normally if we were to do it manually, we would put all the verses together and seperate by 5 lines, but in this 
case we can't do that, so we seperate by 400 characters. Instead of using the doing all at once, we decided to count each element inside the list where all the verses are saved. 
We use a for loop to iterate over that list, and we count the length. While counting the length, we keep adding the verses from the current position inside the list until we 
reach 400 characters. Since the type of data passed through the function is a type **DICT**, we need to iterate twice, the second one being the where the actual verses are at. 
The algorithm we used to complete this task is over complicated cause of the way we keep count. First we keep count by adding, then once the list where all the grouped verses 
are added start to fill up, we count the difference. For example:
```python
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
       holdvalue.append(innerList[loopIterator].encode("utf-8"))
```
In this first **if** statement we check if the length of holdValue is zero, if so, just append the first two verses if and only if they both don't exceed 400 characters, but if they then append the first verse, and right after append the second verse with other ones. The else statement continues with the algorithm, until done.
```python
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
        # DEBUGGING PURPOSES
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
self.testWrite.append(holdvalue)
```
***
Once we are done with everything is ready for use, we send the data to **getData()** function, which will iterate over the list with grouped verses, and join each list. Now 
before any confusion arises, even though we grouped the verses before in the algorithm, the verses still need to be grouped in the form of a string. The reason for this is 
because the algorithm groups the verses like so:
```
[['A','B','C','D']['E','F','G','H']]
 ^---------------^ ^--------------^
      GROUP 1           GROUP 2
```
After we join each element within each group together with spaces added, we return the data back to AJAX which sends the request.
```python
def getData(self):
    self.jsonData = []
    for verses in self.testWrite:
       self.jsonData.append(" ".join(verses))

    return self.jsonData
```
***
# FAQS

**1. Will there be an offline version if we ever need to do it where there is no internet connection?**

A: Currently there is no offline version cause of the way this workds, but we are working on it, and will release it as soon as possible

**2. Is there an application/program that we can use rather than the website?**

A: Currently there is no application/program that you can utilize at the moment because of dependicies that it needs, but we are working on to with the offline version.
