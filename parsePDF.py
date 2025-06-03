import pymupdf
import pymupdf4llm
from pypdf import PdfReader
import numpy as np

inputFile = "Data\\NCT00660673_Prot_000.pdf"

doc = pymupdf.open(inputFile)
reader = PdfReader(inputFile)

idHead = pymupdf4llm.IdentifyHeaders(doc = doc)
#testMarkdown = pymupdf4llm.to_markdown(doc = doc)

#print(testMarkdown)

headingSizes = []

for i in idHead.header_id:
    #print(i)
    headingSizes.append(i)
    #print(idHead.header_id.get(i))

print(headingSizes)

parts = []
firstLine = True
def visitor_body(text, cm, tm, font_dict, font_size):
    y = font_size
    for i in headingSizes:
        if y >= i:
            parts.append(text)
            #print(text)

# Note: theoretically a protocol should not be using negative headings, thus -1 in this case refers to not float
def checkFloat(text):
    try:
        value = float(text)
    except ValueError:
        value = -1
    return value

# Conclude how many/which pages are table of contents
pageCount = 0
tocStart = -1 #Start page# for Table of Contents (Index 0)
tocEnd = -1 #End page# for Table of Contents (Inclusive)
tocIn = False #Bool to check if in Table of Contents
tocHeadNum = -1 #The heading number for Table of Contents (Under the assumption the next header will exit ToC)
for page in reader.pages:
    page.extract_text(visitor_text=visitor_body)
    if len(parts) != 0:
        counter = 0
        #print(parts)
        breaker = True
        while (breaker):
            if parts[counter] == '\n':
                counter += 1
            else:
                breaker = False
        analyst = parts[counter].split()
        restOfText = analyst[1:]
        headerTitle = " ".join(restOfText)
        if headerTitle.lower() == "table of contents" and not tocIn:
            tocStart = pageCount
            tocIn = True
            tocHeadNum = checkFloat(analyst[0])
        #This way of checking should prevent issues with big ToCs
        tempChecker = checkFloat(analyst[0])
        if tempChecker == tocHeadNum + 1 and tocIn:
            tocEnd = pageCount - 1 
            tocIn = False
        parts = []
    pageCount += 1
print(tocStart)
print(tocEnd)
print(tocHeadNum)
print(tocIn)

returnDict = {}
visitorHdNum = []
visitorHdTit = []
visitorHdPg = []
workAround = [False]
#Avoid Page number and header
def visitorToC(text, cm, tm, font_dict, font_size):
    if text != "\n" and text != '':
        tempSplit = text.split()
        if checkFloat(tempSplit[0]) != -1 and len(tempSplit) > 1:
            if checkFloat(tempSplit[0]) == 1.0:
                workAround[0] = True
            if workAround[0]:
                visitorHdNum.append(tempSplit[0])
                if tempSplit[-1].isnumeric():
                    visitorHdPg.append(int(tempSplit[-1]))
                    tempSplit.pop(-1)
                else:
                    numCheck = False
                    strCheck = False
                    newEnd = ""
                    for x in range(0, len(tempSplit[-1])):
                        tempTxt = tempSplit[-1][x:]
                        newTempTxt = tempSplit[-1][:x]
                        if tempTxt.isnumeric() and not numCheck:
                            visitorHdPg.append(int(tempTxt))
                            numCheck = True
                        if not newTempTxt.isalpha() and not strCheck:
                            if len(tempSplit[-1]) != len(newTempTxt):
                                newEnd = tempSplit[-1][:x-1]
                            strCheck = True
                        if strCheck and numCheck:
                            break
                
                    tempSplit.pop(0)
                    tempSplit.pop(-1)
                    tempSplit.append(newEnd)
                #print(text.split())
                visitorHdTit.append(" ".join(tempSplit))

for x in range(tocStart, tocEnd + 1):
    page = reader.pages[x]
    page.extract_text(visitor_text=visitorToC)
    print(visitorHdTit)
    print(visitorHdNum)
    print(visitorHdPg)
    visitorHdTit = []
    visitorHdNum = []
    visitorHdPg = []
    if len(parts) != 0:
        counter = 0
        #print(parts)
        breaker = True
        while (breaker):
            if parts[counter] == '\n':
                counter += 1
            else:
                breaker = False
        analyst = parts[counter].split()
        restOfText = analyst[1:]
        headerTitle = " ".join(restOfText)
        if headerTitle.lower() == "table of contents" and not tocIn:
            tocStart = pageCount
            tocIn = True
            tocHeadNum = checkFloat(analyst[0])
        #This way of checking should prevent issues with big ToCs
        tempChecker = checkFloat(analyst[0])
        if tempChecker == tocHeadNum + 1 and tocIn:
            tocEnd = pageCount - 1 
            tocIn = False

        #print(analyst)
        returnDict[headerTitle] = analyst[0]
        counter += 1
        txtBody = "".join(parts)
        #print(txtBody.split())
        parts = []
    pageCount += 1