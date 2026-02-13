resource "aws_dynamodb_table" "processed_files" {
  name         = "ProcessedFiles"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "FileName"

  attribute {
    name = "FileName"
    type = "S"
  }
}