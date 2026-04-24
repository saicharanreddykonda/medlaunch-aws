# medlaunch-aws
AWS serverless data pipeline for healthcare facility accreditation processing

Project: AWS Serverless Data Pipeline for Expiring Accreditations 

Overview:
This project processes healthcare facility data stored in Amazon S3, identifies facilities with soon-to-expire accreditations, and stores the filtered results back into S3. The workflow is orchestrated using AWS Step Functions and includes error handling with SNS notifications.

Architecture:
S3 (Input) → Step Functions → Lambda → S3 (Output)
↓
SNS (Failure Alerts)

Services Used:

* Amazon S3
* AWS Lambda
* AWS Step Functions
* Amazon SNS
* Amazon CloudWatch

Functionality:

* Reads facility JSON data from S3
* Filters accreditations expiring within 6 months
* Stores processed results in output S3 bucket
* Sends email alerts using SNS on failure

Error Handling:
Implemented using Step Functions Catch block triggering SNS notifications.

Logs & Monitoring:
CloudWatch logs are used for debugging and monitoring Lambda executions.

Cost:
The solution uses serverless services and operates within AWS Free Tier limits.

Author:
Sai Charan Reddy Konda
