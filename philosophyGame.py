import urllib.request as lib
import re

theTree = {}
theTree["https://en.wikipedia.org/wiki/Philosophy"] = [0, ""]
def squirrel(crossSection, style): 
    if crossSection in theTree:
        return theTree[crossSection]
    else:
      theTree[crossSection] = [-1, ""]
      leaf = findLink(crossSection)
      if style == "clean":
        print(crossSection[30:] + " -> " + leaf[30:])
      elif style == "dirty":
        print(crossSection + " -> " + leaf)
      leafDeets = squirrel(leaf, style)
      if leaf[0] == -1:
        return [-1, leaf]
      else:
        theTree[crossSection] = [leafDeets[0] + 1, leaf]
        return theTree[crossSection]
        
def findLink(hyperlink):
  with lib.urlopen(hyperlink) as response:
    text = str(response.read())
    
    #extract all bodies of text
    text = re.sub("<table(.*?)</table>", "", text)
    substrings = re.findall('<p>(.*?)</p>', text)
        
    #filter out text inside parenthese, italics, bolds, tables, supscontainers, and brackets
    cleanPar = ""
    i = 0
    while 'href="' not in cleanPar:
      cleanPar = cleanUp(substrings[i])
      i += 1
    startIndex = cleanPar.index('href="') + 6 #must add six to exclude the href"
    cutText = cleanPar[startIndex:] #cuts the body paragraph from the left side
    endIndex   = cutText.index('"')+len(cleanPar[:startIndex]) #since we cut the body paragraph, the first quote is certainly the end
    newLink = "https://en.wikipedia.org" + cleanPar[startIndex:endIndex]
    return newLink

#filter out unnecessary parts of code
def cleanUp(text):
  text = re.sub("<sup(.*?)</sup>", "", text)
  text = re.sub("<i(.*?)</i>", "", text)
  text = re.sub("<span(.*?)</span>", "", text)
  text = re.sub("<link(.*?)>", "", text)
  text = re.sub("\s\(.*?\)\s", "", text)
  text = re.sub('\s\(.*?\)\,', "", text)
  text = re.sub("\s\(.*?\)\.", "", text)
  text = re.sub('\s\(.*?\)\:', "", text)
  # text = re.sub(".\(.*?\)\s", "", text)
  text = re.sub(',\(.*?\)\,', "", text)
  text = re.sub("\n\(.*?\)\.", "", text)
  return text

def checkForUniqueness(links, new_link):
  if new_link in links:
    return False
  return True

def processInput(inputKey):
  chars = []
  for char in inputKey:
    chars.append(char)
    
  for i in range(len(chars)):
    if chars[i] == " ":
      chars[i] = "_"
  output = ''.join(chars)
  return output

def generateChain(inputKey, style):
  chars = []
  for char in inputKey:
    chars.append(char)
      
  for char in chars:
    if char == " ":
      char = "_"
  inputKey = ''.join(chars)
  
  if style == "clean":
    chain = squirrel("https://en.wikipedia.org/wiki/" + inputKey, "clean")
    return chain
  if style == "dictionary":
    inputKey = processInput(inputKey)
    chain = squirrel("https://en.wikipedia.org/wiki/" + inputKey, "dirty")
    return chain

if __name__ == "__main__":
  print("-> Wikipedia Philosophy Game! <-\n")
  choice = input("1. Generate Pretty Chain From Name\n2. Generate Dictionary Chain From Name\n")
  name = input("\tName: ")
  if choice == "1":
    print("")
    chain = generateChain(name, "clean")[0]
    print(f"\nPhilosophy found after {chain} articles")
  elif choice == "2":
    print("")
    
    chain = generateChain(name, "dictionary")
    print(f"\nPhilosophy found after {chain} articles")