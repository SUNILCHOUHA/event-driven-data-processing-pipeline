import boto3
import os
from datetime import datetime

# AWS Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment Variables from Terraform
TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    """
    Event-Driven File Processing Lambda

    Trigger: S3 ObjectCreated event

    Workflow:
    1. New file uploaded into S3 bucket
    2. Lambda reads file content
    3. Performs basic processing (record count)
    4. Stores metadata into DynamoDB
    5. Generates summary report into S3 reports/ folder

    Note:
    Report files are ignored to prevent recursive triggering.
    """

    # Extract bucket + object key from S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"📌 New file uploaded: {key} in bucket: {bucket}")

    # ✅ Prevent Infinite Loop (Skip Generated Reports)
    if key.startswith("reports/") or key.startswith("daily-reports/"):
        print("⚠️ Skipping report file to avoid recursive processing.")
        return {
            "statusCode": 200,
            "message": "Skipped report file"
        }

    # Download file content from S3
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")
    except Exception as e:
        print(f"❌ Error reading file from S3: {str(e)}")
        return {
            "statusCode": 500,
            "message": "Failed to read file"
        }

    # Basic processing: count lines/records
    total_records = len(content.splitlines())
    print(f"✅ Total records found: {total_records}")

    # Store metadata into DynamoDB
    try:
        table = dynamodb.Table(TABLE_NAME)

        table.put_item(
            Item={
                "FileName": key,
                "Records": total_records,
                "ProcessedAt": datetime.now().isoformat()
            }
        )

        print("✅ Metadata stored successfully in DynamoDB")

    except Exception as e:
        print(f"❌ Error writing to DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "message": "Failed to write metadata"
        }

    # Create report content
    report_text = f"""
File Processing Report
----------------------
File Name      : {key}
Total Records  : {total_records}
Processed Time : {datetime.now().isoformat()}

Status: SUCCESS
"""

    # Save report into S3 reports folder
    report_key = f"reports/{key}-summary.txt"

    try:
        s3.put_object(
            Bucket=bucket,
            Key=report_key,
            Body=report_text
        )

        print(f"📌 Report saved successfully at: {report_key}")

    except Exception as e:
        print(f"❌ Error saving report to S3: {str(e)}")
        return {
            "statusCode": 500,
            "message": "Failed to save report"
        }

    # Final response
    return {
        "statusCode": 200,
        "message": "File processed successfully",
        "input_file": key,
        "total_records": total_records,
        "report_location": report_key
    }