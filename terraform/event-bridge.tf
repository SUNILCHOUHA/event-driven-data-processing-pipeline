resource "aws_cloudwatch_event_rule" "daily_schedule" {
  name                = "daily-report-schedule"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "daily_target" {
  rule      = aws_cloudwatch_event_rule.daily_schedule.name
  target_id = "DailyReportLambda"
  arn       = aws_lambda_function.daily_report.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.daily_report.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_schedule.arn
}