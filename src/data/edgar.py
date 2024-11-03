#from config.settings import *
AWS_ACCESS_KEY_ID = "AKIA3BNTGPX65AXAVA6U"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-west-2"
AGENT_ID = "OBDOASWNGT"
AGENT_ALIAS_ID = "6RSQRHKCPT"
SEC_BUCKET_NAME = "secfedgar-source"
from sec_edgar_downloader import Downloader
import boto3
import os
import shutil

def download_recent_sec_directory_to_s3(stock, limit=2):
    dl = Downloader("Datathon2024", "datathon@polymtl.ca")
    dl.get("DEF 14A", stock, limit=limit, download_details=True)
    dl.get("SC 13G", stock, limit=limit, download_details=True)
    dl.get("SC 13D", stock, limit=limit, download_details=True)
    dl.get("10-K", stock, limit=limit, download_details=True)
    dl.get("8-K", stock, limit=2*limit, download_details=True)

    upload_sec_directory_to_s3(stock, f"{stock}")

# uploads the files to S3 and cleans up the local directory 
def upload_sec_directory_to_s3(stock, s3_directory):
    local_directory = f'./sec-edgar-filings/{stock}'

    s3 = boto3.resource(
        service_name='s3',
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    for root, _, files in os.walk(local_directory):
        for file in files:
            if file == "primary-document.html":
                local_file_path = os.path.join(root, file)
                # Create the relative path for S3
                relative_path = os.path.relpath(local_file_path, local_directory)
                s3_file_path = os.path.join(s3_directory, relative_path)  # Ensure correct path format for S3

                try:
                    s3.Bucket(SEC_BUCKET_NAME).upload_file(local_file_path, s3_file_path)
                    print(f"Uploaded {local_file_path} to s3://{SEC_BUCKET_NAME}/{s3_file_path}")
                except Exception as e:
                    print(f"Failed to upload {local_file_path}: {e}")
        
    shutil.rmtree('./sec-edgar-filings')



download_recent_sec_directory_to_s3("TSLA")


