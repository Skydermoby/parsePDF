import pymupdf
import pymupdf4llm
from pypdf import PdfReader
import numpy as np
import json
import os

os.system('cls')

inputFile = "Data\\NCT00660673_Prot_000.pdf"
outputFile = "extractedTXT.json"

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

visitorHdNum = []
visitorHdTit = []
visitorHdPg = []
workAround = [False]
specialCase = [False]
#Avoid Page number and header
def visitorToC(text, cm, tm, font_dict, font_size):
    if text != "\n" and text != '':
        tempSplit = text.split()
        if specialCase[0]:
            #print(visitorHdTit[-1])
            for x in range(0, len(tempSplit)-1):
                if tempSplit[x].isalpha():
                    tempJoinText = visitorHdTit[-1]
                    visitorHdTit[-1] = " ".join([tempJoinText, tempSplit[x]])
            if (tempSplit[-1].isnumeric()):
                visitorHdPg.append(int(tempSplit[-1]))
            else:
                numCheck = False
                strCheck = False
                newEnd = ""
                for x in range(0, len(tempSplit[-1])):
                    tempTxt = tempSplit[-1][x:]
                    newTempTxt = tempSplit[-1][:x+1]
                    if tempTxt.isnumeric() and not numCheck:
                        visitorHdPg.append(int(tempTxt))
                        numCheck = True
                    if (not newTempTxt.isalpha()) and not strCheck:
                        if len(tempSplit[-1]) != len(newTempTxt):
                            newEnd = tempSplit[-1][:x]
                        strCheck = True
                    if strCheck and numCheck:
                        break
                if not numCheck and not strCheck:
                    print("ERROR: Something went wrong while scraping table of contents")
                else:
                    tempJoinText = visitorHdTit[-1]
                    visitorHdTit[-1] = " ".join([tempJoinText, newEnd])
            specialCase[0] = False
        if checkFloat(tempSplit[0]) != -1 and len(tempSplit) > 1:
            if checkFloat(tempSplit[0]) == 1.0:
                workAround[0] = True
            if workAround[0]:
                visitorHdNum.append(tempSplit[0])
                if tempSplit[-1].isnumeric():
                    visitorHdPg.append(int(tempSplit[-1]))
                    tempSplit.pop(0)
                    tempSplit.pop(-1)
                    tempSplit.pop(-1)
                else:
                    numCheck = False
                    strCheck = False
                    newEnd = ""
                    #print("new")
                    #print(tempSplit)
                    for x in range(0, len(tempSplit[-1])):
                        tempTxt = tempSplit[-1][x:]
                        newTempTxt = tempSplit[-1][:x+1]
                        #print(newTempTxt)
                        #print(strCheck)
                        #print((not newTempTxt.isalpha()) and (not strCheck))
                        if tempTxt.isnumeric() and not numCheck:
                            visitorHdPg.append(int(tempTxt))
                            numCheck = True
                        if (not newTempTxt.isalpha()) and not strCheck:
                            #print("got in")
                            if len(tempSplit[-1]) != len(newTempTxt):
                                newEnd = tempSplit[-1][:x]
                            strCheck = True
                        if strCheck and numCheck:
                            break
                    if not numCheck and not strCheck:
                        specialCase[0] = True
                        tempSplit.pop(0)
                    else:
                        tempSplit.pop(0)
                        tempSplit.pop(-1)
                        tempSplit.append(newEnd)
                    #print(newEnd)
                #print(text.split())
                visitorHdTit.append(" ".join(tempSplit))

for x in range(tocStart, tocEnd + 1):
    page = reader.pages[x]

    page.extract_text(visitor_text=visitorToC)
for x in range(0, len(visitorHdTit)):
    tempText = visitorHdTit[x].split()
    visitorHdTit[x] = " ".join(tempText)

#print(visitorHdTit)
#print(visitorHdNum)
#print(visitorHdPg)

if len(visitorHdTit) != len(visitorHdNum) or len(visitorHdNum) != len(visitorHdPg) or len(visitorHdPg) != len(visitorHdTit):
    print("ERROR: number of headers, titles, and page numbers do not match")

currentBigHeaderIndex = -1
returnDict = []
pageContents = []

def visitor_bodySpecial(text, cm, tm, font_dict, font_size):
    print(text)


for x in range(0, len(visitorHdTit)):
    nextPage = -1
    if x == len(visitorHdNum) - 1:
        nextPage = pageCount - 1
    else:
        nextPage = visitorHdPg[x+1]
    overAllText = ""
    if checkFloat(visitorHdNum[x])%1 == 0:
        returnDict.append({})
        returnDict[-1]["Title"] = visitorHdTit[x]
        returnDict[-1]["Header Number"] = visitorHdNum[x]
        returnDict[-1]["Sub-sections"] = []
        currentBigHeaderIndex = -1
        for y in range(visitorHdPg[x] - 1, nextPage):
            curPage = reader.pages[y]
            curText = curPage.extract_text()
            curText = curText.replace('\n', '')
            if y != nextPage - 1 and y != visitorHdPg[x] - 1:
                overAllText = overAllText + curText
            elif y == nextPage - 1 and y != visitorHdPg[x] - 1:
                if x != len(visitorHdTit) - 1:
                    nextHeader = " ".join([visitorHdNum[x+1], visitorHdTit[x+1]])
                    if nextHeader in curText:
                        curTextSplit = curText.split(nextHeader)
                        overAllText = overAllText + curTextSplit[0]
                    else:
                        overAllText = overAllText + curText
                else:
                    overAllText = overAllText + curText
            elif y == visitorHdPg[x] - 1 and y != nextPage - 1:
                if x != 0:
                    prevHeader = " ".join([visitorHdNum[x], visitorHdTit[x]])
                    if prevHeader in curText:
                        curTextSplit = curText.split(prevHeader)
                        overAllText = overAllText + curTextSplit[-1]
                    else:
                        overAllText = overAllText + curText
                else:
                    overAllText = overAllText + curText
            else:
                #print("Same Page Case: ", visitorHdNum[x])
                nextHeader = " ".join([visitorHdNum[x+1], visitorHdTit[x+1]])
                prevHeader = " ".join([visitorHdNum[x], visitorHdTit[x]])
                if nextHeader in curText:
                    curTextSplit = curText.split(nextHeader)
                    curText = curTextSplit[0]
                if prevHeader in curText:
                    curTextSplit = curText.split(prevHeader)
                    curText = curTextSplit[-1]
                overAllText = overAllText + curText
            if nextPage-1 < visitorHdPg[x]-1:
                print("Someting is wrong: ", visitorHdNum[x])
        returnDict[-1]["Content"] = overAllText
    else:
        returnDict[currentBigHeaderIndex]["Sub-sections"].append({})
        returnDict[currentBigHeaderIndex]["Sub-sections"][-1] = {}
        returnDict[currentBigHeaderIndex]["Sub-sections"][-1]["Title"] = visitorHdTit[x]
        returnDict[currentBigHeaderIndex]["Sub-sections"][-1]["Header Number"] = visitorHdNum[x]
        for y in range(visitorHdPg[x] - 1, nextPage):
            curPage = reader.pages[y]
            curText = curPage.extract_text()
            curText = curText.replace('\n', '')
            if y != nextPage - 1 and y != visitorHdPg[x] - 1:
                overAllText = overAllText + curText
            elif y == nextPage - 1 and y != visitorHdPg[x] - 1:
                if x != len(visitorHdTit) - 1:
                    nextHeader = " ".join([visitorHdNum[x+1], visitorHdTit[x+1]])
                    #print("here", visitorHdNum[x])
                    tester = [nextHeader]
                    #print(tester)
                    #print(curText)
                    #print(nextHeader in curText)
                    if nextHeader in curText:
                        curTextSplit = curText.split(nextHeader)
                        overAllText = overAllText + curTextSplit[0]
                    else:
                        overAllText = overAllText + curText
                else:
                    overAllText = overAllText + curText
            elif y == visitorHdPg[x] - 1 and y != nextPage - 1:
                if x != 0:
                    prevHeader = " ".join([visitorHdNum[x], visitorHdTit[x]])
                    if prevHeader in curText:
                        curTextSplit = curText.split(prevHeader)
                        overAllText = overAllText + curTextSplit[-1]
                    else:
                        overAllText = overAllText + curText
                else:
                    overAllText = overAllText + curText
            else:
                nextHeader = " ".join([visitorHdNum[x+1], visitorHdTit[x+1]])
                prevHeader = " ".join([visitorHdNum[x], visitorHdTit[x]])
                #print("prev", prevHeader)
                #print("next", nextHeader)
                if nextHeader in curText:
                    curTextSplit = curText.split(nextHeader)
                    curText = curTextSplit[0]
                if prevHeader in curText:
                    curTextSplit = curText.split(prevHeader)
                    curText = curTextSplit[-1]
                overAllText = overAllText + curText
        returnDict[currentBigHeaderIndex]["Sub-sections"][-1]["Content"] = overAllText

if os.path.exists(outputFile):
    os.remove(outputFile)

with open(outputFile, "a") as f:
    f.write(json.dumps(returnDict, indent=4))