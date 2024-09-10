from google.cloud import storage
import os
import time


def create_bucket(bucket_name):
    """Creates a new bucket if it doesn't exist."""
    storage_client = storage.Client()

    try:
        bucket = storage_client.bucket(bucket_name)
        if not bucket.exists():
            bucket = storage_client.create_bucket(bucket_name)
            print(f"Bucket {bucket.name} created successfully.")
        else:
            print(f"Bucket {bucket_name} already exists. Skipping creation.")
        return True
    except Exception as e:
        print(f"Error checking/creating bucket: {e}")
        return False

def upload_pdf_to_gcs(bucket_name, source_file_path, destination_blob_name, replace=False):
    """Uploads a PDF file to the specified Google Cloud Storage bucket."""
    storage_client = storage.Client()

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        if blob.exists() and not replace:
            print(f"File {destination_blob_name} already exists in bucket {bucket_name}. Skipping upload.")
            return True

        blob.upload_from_filename(source_file_path)
        print(f"File {source_file_path} {'replaced' if blob.exists() else 'uploaded'} to {destination_blob_name} in bucket {bucket_name}.")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

if __name__ == "__main__":
    bucket_name = "pdfinvoice-bucket"
    source_file_path = r"C:\Users\ANVemuri\Downloads\AmazonBusiness_Invoice.pdf"
    timestamp = int(time.time())
    destination_blob_name = f"invoices/AmazonBusiness_Invoice_{timestamp}.pdf"

    print("Starting addfile.py script...")

    if create_bucket(bucket_name):
        print("Bucket creation successful.")
    else:
        print("Bucket creation failed or bucket already exists.")

    if upload_pdf_to_gcs(bucket_name, source_file_path, destination_blob_name):
        print("File upload successful.")
    else:
        print("File upload failed.")

    print("addfile.py script completed.")