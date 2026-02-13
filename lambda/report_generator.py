import boto3
import os
from datetime import datetime

# AWS Services
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# Environment Variables from Terraform
TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET = os.environ["BUCKET"]
TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    """
    Runs daily using EventBridge scheduler.
    Steps:
    1. Scan DynamoDB table
    2. Generate daily summary report
    3. Save report in S3 daily-reports/
    4. Notify via SNS email
    """

    table = dynamodb.Table(TABLE_NAME)

    # Fetch all processed file records
    response = table.scan()
    items = response.get("Items", [])

    # Build report
    report = "Daily Data Processing Report\n"
    report += "====================================\n"
    report += f"Generated At: {datetime.now()}\n\n"

    if not items:
        report += "No files processed today.\n"
    else:
        report += "Processed Files Summary:\n\n"
        for item in items:
            report += f"- File: {item['FileName']}, Records: {item['Records']}\n"

    # Save daily report into S3
    report_key = f"daily-reports/report-{datetime.now().date()}.txt"

    s3.put_object(
        Bucket=BUCKET,
        Key=report_key,
        Body=report
    )

    print(f"Daily report saved: {report_key}")

    # Send SNS notification
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="Daily Pipeline Report Generated",
        Message=f"Daily report generated successfully.\nLocation: s3://{BUCKET}/{report_key}"
    )

    return {
        "statusCode": 200,
        "message": "Daily report generated and notification sent",
        "report": report_key
    }