import boto3
import s3fs
import pandas as pd




def push_file_to_bucket(filename: str, filekey: str):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id="AKIA3BNTGPX65AXAVA6U",
        aws_secret_access_key="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",
    )

    for bucket in s3.buckets.all():
        print(bucket.name)

    s3.Bucket('sec-edgar-filings-test').upload_file(Filename=filename, Key=filekey)

    for obj in s3.Bucket('sec-edgar-filings-test').objects.all():
        print(obj)

    return None