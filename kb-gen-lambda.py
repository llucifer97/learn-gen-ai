import json, boto3, os, datetime
from botocore.exceptions import ClientError

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="ap-southeast-2")
s3 = boto3.client('s3')

KB_ID = '1JWRVDSFSZ'
MODEL_ARN = 'arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
BUCKET = 'generatedblogwithllm'

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    blog_topic = body['blog_topic']
    
    prompt = f"Write a 400-word blog post on '{blog_topic}'. Use only retrieved context."
    
    resp = bedrock_agent.retrieve_and_generate(
        input={'text': prompt},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': KB_ID,
                'modelArn': MODEL_ARN,  # ✔ REQUIRED
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {'numberOfResults': 4}
                }
            }
        }
    )
    
    blog = resp['output']['text']
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    key = f"blogs/{blog_topic}_{timestamp}.txt"
    s3.put_object(Bucket=BUCKET, Key=key, Body=blog)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'blog_key': key, 'preview': blog[:200]})
    }
