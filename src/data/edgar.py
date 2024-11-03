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

def download_recent_sec_directory_to_s3(stock, limit=1):
    dl = Downloader("Datathon2024", "datathon@polymtl.ca")
    dl.get("DEF 14A", stock, limit=limit, download_details=True)
    dl.get("PRE 14A", stock, limit=limit, download_details=True)
    dl.get("13F-NT", stock, limit=limit, download_details=True)
    dl.get("13F-HR", stock, limit=limit, download_details=True)
    dl.get("13FCONP", stock, limit=limit, download_details=True)
    dl.get("SC 13G", stock, limit=limit, download_details=True)
    dl.get("SC 13D", stock, limit=limit, download_details=True)
    dl.get("10-K", stock, limit=limit, download_details=True)
    dl.get("8-K", stock, limit=limit, download_details=True)
    dl.get("S-1", stock, limit=limit, download_details=True)
    dl.get("S-3", stock, limit=limit, download_details=True)
    dl.get("S-4", stock, limit=limit, download_details=True)
    

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
        
    shutil.rmtree('./sec-edgar-filings', ignore_errors=True)



#download_recent_sec_directory_to_s3("TSLA")


# -*- coding: utf-8 -*-
"""

SEC Filing Scraper
@author: AdamGetbags

"""

# import modules
import requests
import pandas as pd

# create request header
headers = {'User-Agent': "email@address.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(
                           str).str.zfill(10)

for ticker in companyData['ticker']:
    download_recent_sec_directory_to_s3(ticker)