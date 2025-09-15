
#It authenticates to Azure Document Intelligence, runs the prebuilt-layout model on a local image, then prints pages, lines, words (with low-confidence flags), 
# and selection marks.It also attempts to print paragraphs if available, giving you a quick, structured OCR + layout summary of the document.

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import os
from dotenv import load_dotenv

load_dotenv()

endpoint=os.getenv("AZURE_ENDPOINT")
key=os.getenv("AZURE_KEY")


#DocumentAnalysisClient: This is Azure's SDK class for interacting with the Document Intelligence API.
#endpoint: Your Azure Document Intelligence service endpoint URL.
#AzureKeyCredential(key): Authentication method using your API key.

document_analaysis_client=DocumentAnalysisClient(
    endpoint=endpoint,credential=AzureKeyCredential(key)
)

#Reading the file which is available in Local 
#prebuilt-read": Tells Azure to use the Read model, which extracts text (lines and words) from the document.
#poller: Azure returns a polling object because document analysis is an asynchronous process.
#result(): Waits until the analysis is complete and gets the result.

with open("Microsoft_file.jpg","rb") as filet:
    poller=document_analaysis_client.begin_analyze_document("prebuilt-layout",filet)
result=poller.result()

#Loops over each page of the document.
#Prints-->Page number-->Number of lines detected (len(page.lines))-->Number of words detected (len(page.words)
#Each Page-->Lines --> Then Words
for page in result.pages:
    print(f"Document Page{page.page_number} has {len(page.lines)} lines and {len(page.words)} words")

#For each text line Azure found on the page, print its index number and the actual text it contains.
    for i,line in enumerate(page.lines):
        print("Line {}:{}".format(i,line.content))

   
    for word in page.words:
        if word.confidence < 0.92:
             print("Word '{}' has a confidence of {}".format(word.content,word.confidence))

    
    for i,selectionMark in enumerate(page.selection_marks):
        print("SelectionMark {}: {} ({})".format(i+1,selectionMark.state,selectionMark.confidence))


print("****--------------*****")

#Read model does not work with Paragraphs ..so in output None
for paragraph in result.paragraphs:
    print(f"{paragraph.role}: {paragraph.content}")


