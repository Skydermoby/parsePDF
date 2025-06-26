print("5.0 Introduction " in "elated procedures being performed.5.0 IntroductionThe combination of levodopa/carbidopa")

import pymupdf
import pymupdf4llm
import pdfplumber
import pathlib
from pypdf import PdfReader
import numpy as np
import json
import os

fileNames = ["NCT00230607_Prot_000", "NCT00295620_Prot_000", "NCT00310388_Prot_000", "NCT00378482_Prot_000", "NCT434512_Prot_000", "NCT00481091_Prot_000", "NCT00486889_Prot_000", "NCT00543439_Prot_000", "NCT00545532_Prot_000", "NCT00585195_Prot_002", "NCT00556374_Prot_000", "NCT00625378_Prot_000", "NCT00658021_Prot_000", "NCT00660673_Prot_000", "NCT00680992_Prot_000", "NCT00686374_Prot_000", "NCT00700258_Prot_000", "NCT00701701_Prot_000", "NCT00743340_Prot_001", "NCT00761267_Prot_000", "NCT00767819_Prot_000", "NCT00777920_Prot_000", "NCT00790933_Prot_001", "NCT00799266_Prot_000", "NCT00804856_Prot_000", "NCT00810446_Prot_001", "NCT00858364_Prot_001", "NCT00862979_Prot_000"]

os.system('cls')

fileNames = os.listdir('Data\\')

debugMode = False
verboseMode = False
cycleMode = False

fileName = "NCT00658021_SAP_001"

inputFile = "Data\\" + fileName + ".pdf"
outputFile = "Results\\extractedTXT" + fileName + ".json"

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
    doc = pymupdf.open(inputFile)
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

            curDict[-1]["Sub-sections"] = []

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
        inputFile = "Data\\" + fileName + ".pdf"
        outputFile = "Results\\extractedTXT" + fileName + ".json"
        extraction(inputFile, outputFile)
else:
    extraction(inputFile, outputFile)
#page1 = doc[1].get_textpage()

#print(page1.extractTEXT())
#print(doc.get_toc())
#for page in doc:
    #print(page.get_text())