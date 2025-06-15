# AWS Nifty Data Fetch Infrastructure

This repository contains Terraform code and a simple AWS Lambda function to
fetch Nifty index data every 15 minutes. The Lambda function retrieves data
from Yahoo Finance and stores the result in your existing S3 bucket.

## Components

- **Lambda Function** (`infra/lambda_function.py`)
  - Downloads the latest one day 15‑minute data for the Nifty index.
  - Saves the JSON response to an S3 bucket specified by the environment
    variable `BUCKET_NAME` and writes files under the optional
    `DATA_PREFIX`.
- **Terraform** (`infra/main.tf`)
  - Deploys the Lambda function and the IAM permissions it requires.
  - Schedules the function to run every 15 minutes using CloudWatch Events.

## Deployment

1. Install [Terraform](https://www.terraform.io/).
2. Configure your AWS credentials in the environment.
3. Initialize and apply the Terraform configuration:

   ```bash
   cd infra
   terraform init
   terraform apply
   ```

This will deploy the Lambda function, IAM role, and CloudWatch Events rule.
The function writes a file named `<prefix>/YYYY-MM-DD.json` each time it
runs and also updates a master file at `<prefix>/master.json`.
Set the optional `DATA_PREFIX` and `MASTER_KEY` environment variables if you
want to customize where the files are stored within the bucket.

## Notes

- Set the `bucket_name` variable to the name of your existing bucket when
  running `terraform apply`.
- Yahoo Finance data may be subject to change or rate limits. Adapt this
  example to suit your requirements.
- Ensure that the IAM role created by Terraform has only the minimal
  permissions required for security best practices.
