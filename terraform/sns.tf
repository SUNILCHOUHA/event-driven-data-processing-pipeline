resource "aws_sns_topic" "daily_report_topic" {
  name = "daily-report-topic"
}

resource "aws_sns_topic_subscription" "email_sub" {
  topic_arn = aws_sns_topic.daily_report_topic.arn
  protocol  = "email"
  endpoint  = "sunilchouhanw@gmail.com"
}