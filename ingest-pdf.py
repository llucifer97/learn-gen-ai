import json
import boto3
import base64
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'rag-docs-bucket-ayush'  # Your source KB/S3 bucket

def lambda_handler(event, context):
    body = json.loads(event['body'])
    pdf_base64 = body['pdf_data']  # Base64 from client
    filename = body.get('filename', f"upload_{uuid.uuid4()}.pdf")
    
    pdf_bytes = base64.b64decode(pdf_base64)
    
    key = f"docs/{datetime.now().strftime('%Y%m%d')}/{filename}"
    s3.put_object(Bucket=BUCKET, Key=key, Body=pdf_bytes, ContentType='application/pdf')
    
    return {
        'statusCode': 200,
        'body': json.dumps({'s3_key': key, 'message': 'Uploaded & ready for KB sync'})
    }
