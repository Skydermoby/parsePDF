print("5.0 Introduction " in "elated procedures being performed.5.0 IntroductionThe combination of levodopa/carbidopa")

import pymupdf
import pymupdf4llm
import pathlib
from pypdf import PdfReader
import numpy as np
import json
import os

os.system('cls')

debugMode = True
verboseMode = True

inputFile = "Data\\NCT00799266_Prot_000.pdf"
outputFile = "extractedTXT.json"

doc = pymupdf.open(inputFile)
toc = doc.get_toc()

testDict = []
pointer = testDict
for x in range (6):
    testDict.append({})
    testDict[-1]["sub"] = []
    newPoint = testDict[-1]["sub"]
    testDict = newPoint

print(pointer)


curDict = []
topDict = curDict
lastLvl = 1
if len(toc) != 0:
    for x in toc:
        curLvl = x[0]
        curTit = x[1]
        curPg = x[2]
        if lastLvl == curLvl:
            curDict.append({})
            curDict[-1]["Title"] = curTit
            curDict[-1]["Sub-sections"] = []
        elif lastLvl < curLvl:
            newPoint = curDict[-1]["Sub-sections"]
            curDict = newPoint
            curDict.append({})
            curDict[-1]["Title"] = curTit
            curDict[-1]["Sub-sections"] = []
        else: #lastlvl > curLvl
            curDict = topDict
            for x in range(curLvl-1):
                newPoint = curDict[-1]["Sub-sections"]
                curDict = newPoint
            curDict.append({})
            curDict[-1]["Title"] = curTit
            curDict[-1]["Sub-sections"] = []
        lastLvl = curLvl

print(topDict)


if os.path.exists(outputFile):
    os.remove(outputFile)

with open(outputFile, "a") as f:
    f.write(json.dumps(topDict, indent=4))
#page1 = doc[1].get_textpage()

#print(page1.extractTEXT())
#print(doc.get_toc())
#for page in doc:
    #print(page.get_text())