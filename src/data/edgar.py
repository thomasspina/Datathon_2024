from config import settings
from sec_edgar_downloader import Downloader
import boto3
import os
import shutil
import src.models.bedrock_agent as ba
import threading

def download_recent_sec_directory_to_s3(stock):
    settings.sync_finished = False
    dl = Downloader("Datathon2024", "datathon@polymtl.ca")
    dl.get("DEF 14A", stock, limit=1, download_details=True)
    dl.get("DEF 14C", stock, limit=1, download_details=True)
    dl.get("DEFA14A", stock, limit=1, download_details=True)
    dl.get("DEFA14C", stock, limit=1, download_details=True)
    dl.get("10-Q", stock, limit=1, download_details=True)
    dl.get("144", stock, limit=1, download_details=True)
    dl.get("SC 13D", stock, limit=1, download_details=True)
    dl.get("10-K", stock, limit=1, download_details=True)
    dl.get("8-K", stock, limit=1, download_details=True)
    dl.get("3", stock, limit=1, download_details=True)
    dl.get("4", stock, limit=1, download_details=True)
    dl.get("5", stock, limit=1, download_details=True)
    
    upload_sec_directory_to_s3(stock, f"{stock}")

    # Sync the knowledge base with new data
    thread = threading.Thread(
        target=ba.sync_knowledge_base
    )
    thread.start()

# uploads the files to S3 and cleans up the local directory 
def upload_sec_directory_to_s3(stock, s3_directory):
    local_directory = f'./sec-edgar-filings/{stock}'

    s3 = boto3.resource(
        service_name='s3',
        region_name=settings.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    for root, _, files in os.walk(local_directory):
        for file in files:
            if file == "primary-document.txt" or file == "primary-document":
                local_file_path = os.path.join(root, file)
                # Create the relative path for S3
                relative_path = os.path.relpath(local_file_path, local_directory)
                s3_file_path = os.path.join(s3_directory, relative_path)  # Ensure correct path format for S3

                try:
                    s3.Bucket(settings.SEC_BUCKET_NAME).upload_file(local_file_path, s3_file_path)
                    print(f"Uploaded {local_file_path} to s3://{settings.SEC_BUCKET_NAME}/{s3_file_path}")
                except Exception as e:
                    print(f"Failed to upload {local_file_path}: {e}")
        
    shutil.rmtree('./sec-edgar-filings', ignore_errors=True)