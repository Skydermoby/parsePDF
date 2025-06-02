import pymupdf
import pymupdf4llm
from pypdf import PdfReader

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

def visitor_body(text, cm, tm, font_dict, font_size):
    y = font_size
    for i in headingSizes:
        if y >= i:
            parts.append(text)
    print()
            

for page in reader.pages:
    page.extract_text(visitor_text=visitor_body)
    if len(parts) != 0:
        txtBody = "".join(parts)
        print(txtBody.split())
        parts = []

print("1.0".isnumeric())