
#This code connects to Azure Document Intelligence (Form Recognizer), analyzes an image from a URL using the prebuilt-layout model, and prints each page’s line/word counts, the extracted text, low-confidence words, selection marks, and any detected paragraphs.

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint="https://nitishazuredocumentintelligence.cognitiveservices328345nitish.azure.com/"
key="TvAJvcOZMn7JSYtolIb5VeQLTyYejir2C928WilCySJQsSsYhbnitish"


documentUrl = "https://idodata.com/wp-content/uploads/2024/02/MASArticle-scaled.jpg"

#DocumentAnalysisClient: This is Azure's SDK class for interacting with the Document Intelligence API.
#endpoint: Your Azure Document Intelligence service endpoint URL.
#AzureKeyCredential(key): Authentication method using your API key.

document_analaysis_client=DocumentAnalysisClient(
    endpoint=endpoint,credential=AzureKeyCredential(key)
)

#prebuilt-read": Tells Azure to use the Read model, which extracts text (lines and words) from the document.
#poller: Azure returns a polling object because document analysis is an asynchronous process.
#result(): Waits until the analysis is complete and gets the result.

poller=document_analaysis_client.begin_analyze_document_from_url("prebuilt-layout",documentUrl)
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


