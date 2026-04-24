import json
import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client("s3")

INPUT_BUCKET = os.environ["INPUT_BUCKET"]
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]
OUTPUT_KEY = os.environ["OUTPUT_KEY"]


def is_expiring_within_6_months(accreditations):
    today = datetime.utcnow().date()
    threshold = today + timedelta(days=180)

    for accreditation in accreditations:
        valid_until = accreditation.get("valid_until")
        if not valid_until:
            continue

        try:
            expiry_date = datetime.strptime(valid_until, "%Y-%m-%d").date()
            if expiry_date <= threshold:
                return True
        except ValueError:
            print(f"Invalid date format found: {valid_until}")
            continue

    return False


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        key = event.get("key", "raw/facilities.json")

        response = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
        file_content = response["Body"].read().decode("utf-8")

        facilities = json.loads(file_content)

        filtered_facilities = []

        for facility in facilities:
            accreditations = facility.get("accreditations", [])
            if is_expiring_within_6_months(accreditations):
                filtered_facilities.append(facility)

        output_data = {
            "processed_at": datetime.utcnow().isoformat(),
            "total_records": len(facilities),
            "expiring_records": len(filtered_facilities),
            "facilities": filtered_facilities
        }

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=OUTPUT_KEY,
            Body=json.dumps(output_data, indent=2),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "message": "Processing completed successfully",
            "total_records": len(facilities),
            "expiring_records": len(filtered_facilities),
            "output_location": f"s3://{OUTPUT_BUCKET}/{OUTPUT_KEY}"
        }

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise
