output "s3_bucket_name" {
  value = aws_s3_bucket.data_bucket.bucket
}

output "sns_topic_arn" {
  value = aws_sns_topic.daily_report_topic.arn
}

output "dynamodb_table" {
  value = aws_dynamodb_table.processed_files.name
}