import json
import boto3
import datetime
import urllib.request
import os

def lambda_handler(event, context):
    bucket = os.environ['BUCKET_NAME']
    date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?range=1d&interval=15m'
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    s3_key = f'nifty_data/{date_str}.json'
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=s3_key, Body=json.dumps(data).encode('utf-8'))
    return {'status': 'success', 'key': s3_key}
