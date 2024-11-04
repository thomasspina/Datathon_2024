import boto3
from botocore.exceptions import ClientError
import json
from config import settings

def ask_claude(prompt):
    session = boto3.Session(
        aws_access_key_id="AKIA3BNTGPX65AXAVA6U",
        aws_secret_access_key="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",
        region_name="us-west-2",
    )
    bedrock_runtime = session.client(
        "bedrock-runtime", region_name="us-west-2"
    )

    kwargs = {
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100000,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": prompt
            }
            ]
        }
        ]
    })
    }
    response = bedrock_runtime.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    formated_body = format_response(body)
    return formated_body

def format_response(response):
    # Extract and format the content field into a readable string
    content_list = response.get("content", [])
    formatted_text = "\n".join([item["text"] for item in content_list if item["type"] == "text"])
    return formatted_text


def sync_knowledge_base():
    settings.sync_finished = False
    try:
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        bedrock_agent_client = session.client('bedrock-agent', region_name=settings.AWS_DEFAULT_REGION)

        start_job_response = bedrock_agent_client.start_ingestion_job(knowledgeBaseId = settings.KB_ID, dataSourceId = settings.DS_ID)
        job = start_job_response["ingestionJob"]
        while(job['status']!='COMPLETE' ):
                get_job_response = bedrock_agent_client.get_ingestion_job(
                    knowledgeBaseId = settings.KB_ID,
                    dataSourceId = settings.DS_ID,
                    ingestionJobId = job["ingestionJobId"]
                )
                job = get_job_response["ingestionJob"]

        settings.sync_finished = True
        print("Knowledge Base Synced")
        return job

    except ClientError as e:
        raise

def invoke_agent(session_id, prompt):
    try:
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        bedrock_runtime = session.client(
            "bedrock-agent-runtime", region_name="us-west-2"
        )

        response = bedrock_runtime.invoke_agent(
            agentId=settings.AGENT_ID,
            agentAliasId=settings.AGENT_ALIAS_ID,
            enableTrace=True,
            sessionId=session_id,
            inputText=prompt,
        )

        full_response = ''
        for chunk in response['completion']:
            if 'chunk' in chunk:
                text = chunk['chunk']['bytes'].decode()
                full_response += text

        return full_response

    except ClientError as e:
        raise

    
