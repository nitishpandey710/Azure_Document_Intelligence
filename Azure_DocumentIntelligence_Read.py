
#It performs OCR on a remote document using Azure’s prebuilt-read model and outputs detected lines, words with confidence, and page-level details.
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint="https://nitishpandeyazuredocumentintelligenceabc.cognitiveservices.azure.com/"
key="TvAJvcOZMn7JSYtolIb5VeQLTyYejir2C928WilCynitishpandey"


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

poller=document_analaysis_client.begin_analyze_document_from_url("prebuilt-read",documentUrl)
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
        print("Word '{}' has a confidence of {}".format(word.content,word.confidence))


print("****--------------*****")

#Read model does not work with Paragraphs ..so in output None
for paragraph in result.paragraphs:
    print(f"{paragraph.role}: {paragraph.content}")


