import json
import boto3

def lambda_handler(event, context):
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-south-1')
    model_id = 'meta.llama3-8b-instruct-v1:0'
    
    prompt = event.get('prompt', 'Generate a simple text.')
    formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    
    body = json.dumps({
        'prompt': formatted_prompt,
        'max_gen_len': 512,
        'temperature': 0.5,
        'top_p': 0.9
    })
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body,
            contentType='application/json',
            accept='application/json'
        )
        result = json.loads(response['body'].read())
        output_text = result['generation']
        
        return {
            'statusCode': 200,
            'body': json.dumps({'generated_text': output_text})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
