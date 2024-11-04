import boto3
from botocore.exceptions import ClientError
import json
from config import settings
import streamlit as st

class BedrockAgent:
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_region_name = settings.AWS_DEFAULT_REGION
    session_id = None

<<<<<<< HEAD
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
=======
    @classmethod
    def set_session_id(cls, session_id):
        cls.session_id = session_id

    @classmethod
    def talk_to_model(cls, history_messages=[]):
>>>>>>> fac32de98f604982c43298f42c2c0af40d52b82f
        session = boto3.Session(
            aws_access_key_id=cls.aws_access_key_id,
            aws_secret_access_key=cls.aws_secret_access_key,
            region_name=cls.aws_region_name,
        )
        bedrock_runtime = session.client(
            "bedrock-runtime", region_name="us-west-2"
        )

        # if len(history_messages) == 0:
        #     history_messages = [{
        #     "role": "user",
        #     "content": [
        #         {
        #             "type": "text",
        #             "text": prompt
        #         }
        #         ]
        #     }]
        # else:
        #     history_messages.append({
        #     "role": "user",
        #     "content": [
        #         {
        #             "type": "text",
        #             "text": prompt
        #         }
        #         ]
        #     })

<<<<<<< HEAD
        full_response = ''
        for chunk in response['completion']:
            if 'chunk' in chunk:
                text = chunk['chunk']['bytes'].decode()
                full_response += text

        return full_response
=======


        kwargs = {
        "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": history_messages
        })
        }
        response = bedrock_runtime.invoke_model(**kwargs)
        body = json.loads(response['body'].read())
        formated_body = cls.format_response(body)
        return formated_body
    
    @classmethod
    def send_news(cls, symbol, news):
        news_prompt = f"Here are the latest news titles for the {symbol}: {news}"
>>>>>>> fac32de98f604982c43298f42c2c0af40d52b82f

        st.session_state.messages.append({"role": "user", "content": news_prompt})

<<<<<<< HEAD
    
=======
        # Feeding the model with the latest news
        news_response = BedrockAgent.talk_to_model(st.session_state.messages)
        st.session_state.messages.append({
                            "role": "assistant",
                            "content": news_response
                        })
                

    @classmethod
    def send_stats(cls, symbol, stats):
        stats_prompt = f"Here are the key stats for the {symbol}: {stats}"

        st.session_state.messages.append({"role": "user", "content": stats_prompt})
        # Feeding the model with the latest stats
        stats_response = BedrockAgent.talk_to_model(st.session_state.messages)
        st.session_state.messages.append({
            "role": "assistant",
            "content": stats_response
        })

    @classmethod
    def format_response(cls, response):
        # Extract and format the content field into a readable string
        content_list = response.get("content", [])
        formatted_text = "\n".join([item["text"] for item in content_list if item["type"] == "text"])
        return formatted_text

    @classmethod
    def invoke_agent(cls, session_id, prompt):
        try:
            session = boto3.Session(
                aws_access_key_id=cls.aws_access_key_id,
                aws_secret_access_key=cls.aws_secret_access_key,
                region_name=cls.aws_region_name,
            )
            bedrock_runtime = session.client(
                "bedrock-agent-runtime", region_name="us-west-2"
            )

            response = bedrock_runtime.invoke_agent(
                agentId=settings.AGENT_ID,
                agentAliasId=settings.AGENT_ALIAS_ID,
                enableTrace=True,
                sessionId=cls.session_id,
                inputText=prompt,
            )

            output_text = ""
            citations = []
            trace = {}

            has_guardrail_trace = False
            for event in response.get("completion"):
                # Combine the chunks to get the output text
                if "chunk" in event:
                    chunk = event["chunk"]
                    output_text += chunk["bytes"].decode()
                    if "attribution" in chunk:
                        citations = citations + chunk["attribution"]["citations"]

                # Extract trace information from all events
                if "trace" in event:
                    for trace_type in [
                        "guardrailTrace",
                        "preProcessingTrace",
                        "orchestrationTrace",
                        "postProcessingTrace",
                    ]:
                        if trace_type in event["trace"]["trace"]:
                            mapped_trace_type = trace_type
                            if trace_type == "guardrailTrace":
                                if not has_guardrail_trace:
                                    has_guardrail_trace = True
                                    mapped_trace_type = "preGuardrailTrace"
                                else:
                                    mapped_trace_type = "postGuardrailTrace"
                            if trace_type not in trace:
                                trace[mapped_trace_type] = []
                            trace[mapped_trace_type].append(
                                event["trace"]["trace"][trace_type]
                            )

        except ClientError as e:
            raise

        return {"output_text": output_text}
>>>>>>> fac32de98f604982c43298f42c2c0af40d52b82f
