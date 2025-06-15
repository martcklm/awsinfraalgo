# AWS Nifty Data Fetch Infrastructure

This repository contains Terraform code and a simple AWS Lambda function to
fetch Nifty index data at a 15 minute interval each day. The Lambda function
retrieves data from Yahoo Finance and stores the result in an S3 bucket.

## Components

- **Lambda Function** (`infra/lambda_function.py`)
  - Downloads the latest one day 15‑minute data for the Nifty index.
  - Saves the JSON response to an S3 bucket specified by the environment
    variable `BUCKET_NAME`.
- **Terraform** (`infra/main.tf`)
  - Creates an S3 bucket for the data.
  - Deploys the Lambda function.
  - Schedules the function to run daily using CloudWatch Events.

## Deployment

1. Install [Terraform](https://www.terraform.io/).
2. Configure your AWS credentials in the environment.
3. Initialize and apply the Terraform configuration:

   ```bash
   cd infra
   terraform init
   terraform apply
   ```

This will provision the S3 bucket, Lambda function, IAM role, and CloudWatch
Events rule. The function will execute once per day and store the data in the
bucket under `nifty_data/YYYY-MM-DD.json`.

## Notes

- Yahoo Finance data may be subject to change or rate limits. Use this example
  as a starting point and adapt it as necessary for your use case.
- Ensure that the IAM role created by Terraform has only the minimal
  permissions required for security best practices.
