
#This script connects to Azure Blob Storage, downloads every PDF in a container, analyzes each using Azure Document Intelligence (prebuilt-document), extracts key-value pairs, and saves the results as JSON files in a local folder.
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get credentials from environment variables (recommended for security)
endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

storage_connection_string ="DefaultEndpointsProtocol=https;AccountName=slbstorarF7jT53X7SEFhA6sUypointSuffix=core.windows.net"
container_name = "drillingreport"

# Initialize clients
blob_client = BlobServiceClient.from_connection_string(storage_connection_string)
container_client = blob_client.get_container_client(container_name)
form_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Create local folder for output
os.makedirs("extracted_json", exist_ok=True)

# Process all PDFs
blob_list = container_client.list_blobs()

for blob in blob_list:
    if blob.name.endswith('.pdf'):
        try:
            print(f"Processing: {blob.name}")
            
            # Download PDF content directly
            pdf_data = container_client.download_blob(blob.name).readall()
            
            # Analyze PDF
            poller = form_client.begin_analyze_document("prebuilt-document", document=pdf_data)
            result = poller.result()
            
            # Extract key-value pairs
            extracted_data = {}
            for kv in result.key_value_pairs:
                if kv.key and kv.value:
                    key = kv.key.content.strip()
                    value = kv.value.content.strip()
                    extracted_data[key] = value
            
            # Save JSON file
            json_filename = blob.name.replace('.pdf', '.json')
            json_path = f"extracted_json/{json_filename}"
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            print(f" Saved: {json_path}")
            
        except Exception as e:
            print(f" Error with {blob.name}: {e}")

print("All files processed")