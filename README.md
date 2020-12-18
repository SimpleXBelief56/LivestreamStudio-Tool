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

