from google.cloud import storage
from google.cloud import documentai_v1 as documentai
import json

# def upload_pdf_to_gcs(bucket_name, source_file_path, destination_blob_name, replace=False):
#     # ... (keep the existing upload function as is) ...

def process_document(project_id, location, processor_id, bucket_name, blob_name):
    """Downloads a document from GCS, processes it with Document AI, and returns the extracted data as JSON."""
    storage_client = storage.Client()
    documentai_client = documentai.DocumentProcessorServiceClient()

    # Download the document from GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    document_content = blob.download_as_bytes()

    # Prepare the request for Document AI
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    raw_document = documentai.RawDocument(content=document_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    # Process the document
    result = documentai_client.process_document(request=request)
    document = result.document

    # Extract and structure the data
    extracted_data = {}
    for entity in document.entities:
        extracted_data[entity.type_] = entity.mention_text

    return json.dumps(extracted_data, indent=2)

# def main():
#     #