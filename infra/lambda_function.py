import json
import boto3
import datetime
import urllib.request
import os


def _fetch_data() -> dict:
    """Download the latest Nifty data from Yahoo Finance."""
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
        "?range=1d&interval=15m"
    )
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def lambda_handler(event, context):
    bucket = os.environ["BUCKET_NAME"]
    prefix = os.environ.get("DATA_PREFIX", "nifty-15min-data")
    master_key = os.environ.get("MASTER_KEY", f"{prefix}/master.json")

    date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data = _fetch_data()

    s3 = boto3.client("s3")

    daily_key = f"{prefix}/{date_str}.json"
    s3.put_object(
        Bucket=bucket, Key=daily_key, Body=json.dumps(data).encode("utf-8")
    )

    try:
        existing = s3.get_object(Bucket=bucket, Key=master_key)
        master_data = json.loads(existing["Body"].read().decode("utf-8"))
    except s3.exceptions.NoSuchKey:
        master_data = []

    updated = False
    for entry in master_data:
        if entry.get("date") == date_str:
            entry["data"] = data
            updated = True
            break
    if not updated:
        master_data.append({"date": date_str, "data": data})

    s3.put_object(
        Bucket=bucket, Key=master_key, Body=json.dumps(master_data).encode("utf-8")
    )

    return {"status": "success", "daily_key": daily_key, "master_key": master_key}
