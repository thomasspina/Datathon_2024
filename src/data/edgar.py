
from sec_edgar_downloader import Downloader
import boto3
import os

def upload_directory_to_s3(local_directory, bucket_name, s3_directory):
    s3 = boto3.resource(
        service_name='s3',
        region_name="us-west-2",
        aws_access_key_id="AKIA3BNTGPX65AXAVA6U",
        aws_secret_access_key="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"
    )

    

    for root, _, files in os.walk(local_directory):
        for file in files:
            if file == "primary-document.html":
                local_file_path = os.path.join(root, file)
                # Create the relative path for S3
                relative_path = os.path.relpath(local_file_path, local_directory)
                s3_file_path = os.path.join(s3_directory, relative_path)  # Ensure correct path format for S3

                try:
                    s3.Bucket(bucket_name).upload_file(local_file_path, s3_file_path)
                    print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
                except Exception as e:
                    print(f"Failed to upload {local_file_path}: {e}")


dl = Downloader("MyCompanyName", "my.email@domain.com")

# step 1: get relavant SEC filings
stock = "AAPL"
# dl.get("DEF 14A", stock, limit=2, download_details=True)
# dl.get("SC 13G", stock, limit=2, download_details=True)
# dl.get("SC 13D", stock, limit=2, download_details=True)
# dl.get("10-K", stock, limit=3, download_details=True)
# dl.get("8-K", stock, limit=3, download_details=True)

local_directory = f'./sec-edgar-filings/{stock}'
bucket_name = 'secfedgar-source'
s3_directory = f'{stock}'

# session = boto3.Session(
#     aws_access_key_id="AKIA3BNTGPX65AXAVA6U",
#     aws_secret_access_key="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",
#     region_name="us-west-2"
# )

upload_directory_to_s3(local_directory, bucket_name, s3_directory)




