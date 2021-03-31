# Reference:
# GA API CONNECT: https://serhiipuzyrov.com/2020/11/how-to-import-cost-data-into-google-analytics-using-python-and-api/
# Lambda function import 3rd-party packages: https://dev.to/mmascioni/using-external-python-packages-with-aws-lambda-layers-526o
# https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/uploads/uploadData
# https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py

import os
import json
import urllib.parse
import boto3
from pandas import read_csv
from io import StringIO, BytesIO
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build


print('Loading function')

s3 = boto3.client('s3')

# fill these variables with your values
key_file_location = '/opt/python/service_account.json'
scopes = ['https://www.googleapis.com/auth/analytics',
          'https://www.googleapis.com/auth/analytics.edit']
account_id = 'YourAccountID'
property_id = 'YourPropertyID'
dataset_id = 'YourDatasetID'
    
# change this mapping to your csv column-to-ga dimensions 
cols = {'col1': 'ga:dimension9', 'col2': 'ga:dimension67'}


def upload_to_ga(df):
    
    credentials = service_account.Credentials.from_service_account_file(filename=key_file_location, scopes=scopes)
    analytics = build('analytics', 'v3', credentials=credentials)
    
    df = df[list(cols.keys())]
    df.rename(columns=cols, inplace=True)
    # upload to GA
    io_df = BytesIO()
    df.to_csv(io_df, index=False, encoding='utf-8')
    media = MediaIoBaseUpload(io_df, mimetype='application/octet-stream', resumable=False)
    daily_upload = analytics.management().uploads().uploadData(
        accountId=account_id,
        webPropertyId=property_id,
        customDataSourceId=dataset_id,
        media_body=media).execute()


def lambda_handler(event, context):
    event_types = ['ObjectCreated:CompleteMultipartUpload', 'ObjectCreated:Copy', 'ObjectCreated:Put']
    if event['Records'][0]['eventName'] in event_types:
        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    else:
        raise ValueError('Only [CopyObject], [PutObject] and [CompleteMultipartUpload] operations currently supported.')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        response = response["Body"].read()
        df = read_csv(BytesIO(response), encoding='utf-8')
        upload_to_ga(df)
        return 'File has been successfully uploaded!'
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
