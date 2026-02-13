# Event-Driven Data Processing Pipeline on AWS (Terraform + Lambda)

An **event-driven cloud-native data processing pipeline** built on AWS that automatically captures uploaded files, processes them using AWS Lambda, stores metadata in DynamoDB, and generates summary reports in S3 — fully provisioned using **Terraform** and automated with **GitHub Actions CI/CD**.

---

## 📌 Project Overview

This project demonstrates a real-world **serverless event-driven architecture** where incoming data files trigger automated processing and reporting workflows.

Whenever a CSV/JSON file is uploaded into an S3 bucket:

- AWS Lambda processes the file
- Metadata is stored in DynamoDB
- A summary report is generated and saved back into S3
- Daily reporting is supported using EventBridge scheduling
- Notifications can be delivered using Amazon SNS

---

## 🏗️ High-Level Architecture

**Workflow:**

1. User uploads file → **Amazon S3**
2. S3 triggers an **ObjectCreated Event**
3. Event invokes **Lambda File Processor**
4. Lambda extracts metadata (record count, timestamp)
5. Metadata stored in **DynamoDB**
6. Summary report saved in **S3 reports/** folder
7. EventBridge runs daily scheduled reporting job
8. Optional SNS email notification

---

## ⚙️ AWS Services Used

- **Amazon S3** – Raw file storage + processed reports
- **AWS Lambda** – Serverless processing & report generation
- **Amazon DynamoDB** – Metadata storage for processed files
- **Amazon EventBridge** – Daily scheduled automation
- **Amazon SNS** – Email notification support
- **IAM Roles & Policies** – Secure access control
- **CloudWatch Logs** – Monitoring and debugging

---

## 📁 Project Structure

```bash
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
│
├── lambda/
│   ├── processor.py            # File processing Lambda
│   ├── processor.zip
│   ├── report_generator.py     # Daily report Lambda
│   └── report_generator.zip
│
├── terraform/
│   ├── main.tf                 # Provider + core config
│   ├── s3.tf                   # S3 bucket resources
│   ├── dynamodb.tf             # DynamoDB table resources
│   ├── lambda.tf               # Lambda functions + triggers
│   ├── iam.tf                  # IAM roles & permissions
│   ├── event-bridge.tf         # EventBridge scheduling
│   ├── sns.tf                  # SNS topic + subscription
│   ├── output.tf               # Terraform outputs
│   └── terraform.tfstate       # Local state (remove before submission)
│
└── sample.csv                  # Sample input file
🚀 Deployment (Terraform)
1️⃣ Configure AWS CLI
aws configure

Ensure your IAM user/role has access to:
S3
Lambda
DynamoDB
EventBridge
SNS
IAM


2️⃣ Initialize Terraform
cd terraform
terraform init
3️⃣ Validate Configuration
terraform validate
4️⃣ Plan Infrastructure
terraform plan
5️⃣ Apply Infrastructure
terraform apply -auto-approve
📤 Testing the Pipeline
Upload a File to S3
aws s3 cp sample.csv s3://<your-bucket-name>/
Verify Report Output
aws s3 ls s3://<your-bucket-name>/reports/

Download report:
aws s3 cp s3://<your-bucket-name>/reports/sample.csv-summary.txt -
Verify DynamoDB Entry
aws dynamodb scan --table-name ProcessedFiles --region ap-south-1

🔄 CI/CD Automation (GitHub Actions)
This repository includes a GitHub Actions workflow that supports:
Terraform Init & Validate
Terraform Plan on Pull Requests
Manual Terraform Apply via workflow_dispatch
CI/CD Pipeline File:

.github/workflows/deploy.yml
📌 Key Learning Outcomes

Event-driven architecture using AWS native services
Serverless file processing with AWS Lambda
Infrastructure automation using Terraform (IaC)
Metadata tracking using DynamoDB
Automated deployments with GitHub Actions CI/CD
Real-world reporting workflow with S3 + EventBridge

📎 Deliverables
✔ Research Report
✔ Architecture Diagram & Justification
✔ Complete Terraform Infrastructure Code
✔ Lambda Processing Scripts
✔ Code Walkthrough Video Demo

👤 Author

Sunil Chouhan
Cloud & DevOps Enthusiast | AWS | Terraform | CI/CD | GitOps
