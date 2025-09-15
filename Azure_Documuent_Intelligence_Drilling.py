
#This code uses Azure Document Intelligence’s prebuilt-document model to analyze a local PDF, extract key-value pairs, and save the results as a JSON file.

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get credentials from environment variables (recommended for security)
endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

# Initialize the Document Analysis Client
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Path to your local PDF file
file_path = r"C:\Users\Nitish\Desktop\Azure\Azure_DocIntelligence\Python\SLB_Drilling_report.pdf"

try:
    # Read and analyze the file
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", document=f)
        result = poller.result()

    # Extract key-value pairs
    key_value_pairs = {}
    for kv in result.key_value_pairs:
        if kv.key and kv.value:
            key = kv.key.content.strip()
            value = kv.value.content.strip()
            key_value_pairs[key] = value

    # Output as JSON (print to console)
    json_output = json.dumps(key_value_pairs, indent=2, ensure_ascii=False)
    print(json_output)

    # *** NEW: Write to JSON file ***
    output_file = "drilling_report_extracted.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json_file.write(json_output)
    print(f"\n JSON output saved to {output_file}")

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error: {e}")