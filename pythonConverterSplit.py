print("5.0 Introduction " in "elated procedures being performed.5.0 IntroductionThe combination of levodopa/carbidopa")

import pymupdf
import pymupdf4llm
import pdfplumber
import pathlib
from pypdf import PdfReader
import numpy as np
import json
import os


os.system('cls')

fileNames = os.listdir('Data\\')

debugMode = False
verboseMode = False
cycleMode = False

fileName = "NCT00658021_SAP_001"

inputFile = "Data\\" + fileName + ".pdf"
outputFile = "Results\\FLAT" + fileName + ".json"

tableExtractor = pdfplumber.open(inputFile)

print(tableExtractor)

def checkHeader(text):
    stillHeader = True
    for x in text:
        if (not x.isdigit()) and x != ".":
            stillHeader = False
            break
    return stillHeader


def printError(text):
    print("Something wrong has occured:", text, ". This error took place in:", fileName)



def extraction(inputFile, outputFile):
    inputFile = "Data\\" + fileName + ".pdf"
    doc = pymupdf.open(inputFile)
    docName = doc.metadata["title"]
    toc = doc.get_toc()

    if debugMode:
        print(toc)

    testDict = []
    pointer = testDict
    breakerControl = 0

    curDict = []
    topDict = curDict
    lastLvl = 1
    if len(toc) != 0:
        pgCounter = 0
        secNameList = ["Top"]
        secNumList = ["Top"]
        lastName = ""
        lastNum = ""
        for x in toc:
            curLvl = x[0]
            curTit = x[1]
            curPg = int(x[2])
            
            if lastLvl < curLvl:
                secNameList.append(lastName)
                secNumList.append(lastNum)
            elif lastLvl > curLvl:
                secNameList.pop()
                secNumList.pop()
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
            curDict[-1]["File Name"] = inputFile
            curDict[-1]["Report Name"] = docName
            curDict[-1]["Parent Name"] = secNameList[-1]
            curDict[-1]["Parent Num"] = secNumList[-1]
            lastName = curName
            lastNum = curHd
            
            nxtPg = -1
            if pgCounter != len(toc) -1:
                nxtPg = int(toc[pgCounter + 1][2])
            else:
                nxtPg = len(doc)
            if nxtPg == -1:
                printError("Next page number captured incorrectly")

            if debugMode:
                print("fortnite", curPg, nxtPg)
            
            firstPage = doc[curPg-1].get_textpage()
            retFirstPg = firstPage.extractText()
            retFirstPg = retFirstPg.replace('\n', '')
            splitVile = retFirstPg.split(curTit)
            if len(splitVile) != 1 and verboseMode:
                print("this happened at", pgCounter)
            splitVile.pop(0)
            if breakerControl == 0 and debugMode:
                print("".join(splitVile))
                
            curContent = []
            curContent.append("".join(splitVile))
            for x in range(curPg, nxtPg - 1):
                curPage = doc[x].get_textpage()
                curTB = doc[x].find_tables()
                print(curTB.tables)
                curContent.append(curPage.extractText())
            if pgCounter != len(toc)-1:
                nextTit = toc[pgCounter+1][1]
                lastPage = doc[nxtPg-1].get_textpage()
                retLastPg = lastPage.extractText()
                retLastPg = retLastPg.replace('\n', '')
                splitVile = retLastPg.split(nextTit)
                splitVile.pop(-1)
                curContent.append("".join(splitVile))

            if curPg == nxtPg:
                if verboseMode:
                    print("this happened aaaaaaaaaaaaat", curTit)
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
                curContent = ["".join(splitVile)]
            
            curCont = "".join(curContent)

            curDict[-1]["Content"] = curCont

            lastLvl = curLvl
            pgCounter += 1
            breakerControl =1
    else:
        printError("TOC length is 0 :(")
        topDict = ["Could not find ToC"]
    if verboseMode:
        print(topDict)


    if os.path.exists(outputFile):
        os.remove(outputFile)

    with open(outputFile, "a") as f:
        f.write(json.dumps(topDict, indent=4))



if cycleMode:
    for file in fileNames:
        print("Now running:", file)
        fileName = file.replace(".pdf", "")
        outputFile = "Results\\extractedTXT" + fileName + ".json"
        extraction(fileName, outputFile)
else:
    extraction(fileName, outputFile)
