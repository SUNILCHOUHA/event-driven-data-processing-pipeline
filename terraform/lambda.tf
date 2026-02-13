resource "aws_lambda_function" "file_processor" {
  function_name = "file-processor-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "processor.lambda_handler"
  runtime       = "python3.9"

  filename         = "../lambda/processor.zip"
  source_code_hash = filebase64sha256("../lambda/processor.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.processed_files.name
      BUCKET     = aws_s3_bucket.data_bucket.bucket
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.data_bucket.arn
}


resource "aws_lambda_function" "daily_report" {
  function_name = "daily-report-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "report_generator.lambda_handler"
  runtime       = "python3.9"

  filename         = "../lambda/report_generator.zip"
  source_code_hash = filebase64sha256("../lambda/report_generator.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.processed_files.name
      BUCKET     = aws_s3_bucket.data_bucket.bucket
      TOPIC_ARN  = aws_sns_topic.daily_report_topic.arn
    }
  }
}