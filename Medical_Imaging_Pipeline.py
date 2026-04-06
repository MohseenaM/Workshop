# lambda_imaging_pipeline.py
import json
import boto3
import os
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()

s3 = boto3.client('s3')
medical_imaging = boto3.client('medical-imaging')  # boto3 client name: 'medical-imaging'
bedrock = boto3.client('bedrock-runtime')

DATASTORE_ID = os.environ['HEALTHIMAGING_DATASTORE_ID']
BUCKET = os.environ['S3_BUCKET']

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # 1. Security: IAM role only allows s3:GetObject + medical-imaging:ImportDICOM + kms:Decrypt
        logger.info(f"Processing DICOM: s3://{bucket}/{key}")
        
        # 2. Import to HealthImaging (Reliability + Performance)
        import_job = medical_imaging.start_dicom_import_job(
            DatastoreId=DATASTORE_ID,
            InputS3Uri=f"s3://{bucket}/{key}",
            OutputS3Uri=f"s3://{BUCKET}/imports/",
            JobName=f"import-{key.split('/')[-1]}"
        )
        
        job_id = import_job['JobId']
        logger.info(f"Import job started: {job_id}")
        
        # 3. Optional: Use Bedrock to summarize metadata (Operational Excellence + Cost)
        # Fetch metadata via GetImageSet (example)
        summary = bedrock.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": f"Summarize this DICOM study: {key}"}]
            })
        )
        
        # 4. CloudWatch custom metric (Observability)
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_data(
            Namespace='HealthImaging/Workshop',
            MetricData=[{
                'MetricName': 'DICOMImports',
                'Value': 1,
                'Unit': 'Count',
                'Dimensions': [{'Name': 'DatastoreId', 'Value': DATASTORE_ID}]
            }]
        )
    
    return {"statusCode": 200, "body": json.dumps({"jobId": job_id})}
