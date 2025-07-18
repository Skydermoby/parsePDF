import pymupdf
import pymupdf4llm
import pdfplumber
import pathlib
from pypdf import PdfReader
import numpy as np
import json
import os

def checkHeader(text):
    stillHeader = True
    for x in text:
        if (not x.isdigit()) and x != ".":
            stillHeader = False
            break
    return stillHeader


def printError(text):
    print("Something wrong has occured:", text)



def extraction(inputFile):
    #doc = pymupdf.open(stream=inputFile.read())
    doc = pymupdf.open(inputFile)
    toc = doc.get_toc()

    testDict = []
    pointer = testDict
    breakerControl = 0

    curDict = []
    topDict = curDict
    lastLvl = 1
    if len(toc) != 0:
        pgCounter = 0
        for x in toc:
            curLvl = x[0]
            curTit = x[1]
            curPg = int(x[2])
            
            if lastLvl < curLvl:
                newPoint = curDict[-1]["Sub-sections"]
                curDict = newPoint
            elif lastLvl > curLvl:
                curDict = topDict
                for x in range(curLvl-1):
                    newPoint = curDict[-1]["Sub-sections"]
                    curDict = newPoint
            curDict.append({})
            curSplit = curTit.split()
            curHd = "-1"
            curName = "-1"
            if checkHeader(curSplit[0]):
                curHd = curSplit[0]
                curSplit.pop(0)
                curName = " ".join(curSplit)
            else:
                curHd = "N/A"
                curName = curTit
            if curHd == "-1":
                printError("Header Number bypassed Checker")
            curDict[-1]["Header Number"] = curHd
            curDict[-1]["Title"] = curName
            
            
            nxtPg = -1
            if pgCounter != len(toc) -1:
                nxtPg = int(toc[pgCounter + 1][2])
            else:
                nxtPg = len(doc)
            if nxtPg == -1:
                printError("Next page number captured incorrectly")
            
            firstPage = doc[curPg-1].get_textpage()
            retFirstPg = firstPage.extractText()
            retFirstPg = retFirstPg.replace('\n', '')
            splitVile = retFirstPg.split(curTit)
            splitVile.pop(0)
                
            curContent = []
            curContent.append("".join(splitVile))
            for x in range(curPg, nxtPg - 1):
                curPage = doc[x].get_textpage()
                curTB = doc[x].find_tables()
                print(curTB.tables)
                returnText = curPage.extractText().replace('\n', '')
                curContent.append(returnText)
            if pgCounter != len(toc)-1:
                nextTit = toc[pgCounter+1][1]
                lastPage = doc[nxtPg-1].get_textpage()
                retLastPg = lastPage.extractText()
                retLastPg = retLastPg.replace('\n', '')
                splitVile = retLastPg.split(nextTit)
                splitVile.pop(-1)
                curContent.append("".join(splitVile))

            if curPg == nxtPg:
                firstPage = doc[curPg-1].get_textpage()
                retFirstPg = firstPage.extractText()
                retFirstPg = retFirstPg.replace('\n', ' ')
                
                splitVile = retFirstPg.split(curTit)
                if len(splitVile) == 1:
                    splitVile = retFirstPg.split(curName)
                splitVile.pop(0)
                splitVile = "".join(splitVile)
                splitVile = splitVile.split(nextTit) 
                splitVile.pop(-1)
                curContent = ["".join(splitVile).replace('\n','')]
            
            curCont = "".join(curContent)

            curDict[-1]["Content"] = curCont

            curDict[-1]["Sub-sections"] = []

            lastLvl = curLvl
            pgCounter += 1
            breakerControl =1
    else:
        printError("TOC length is 0 :(")
        topDict = ["Could not find ToC"]
    #return topDict
    return json.dumps(topDict, indent=4)
