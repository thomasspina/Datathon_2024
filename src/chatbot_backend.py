from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock
import boto3
import os
import pandas as pd

access_df = pd.read_csv("../admin_accessKeys.csv")
os.environ["AWS_ACCESS_KEY_ID"] = access_df["Access key ID"][0]
os.environ["AWS_SECRET_ACCESS_KEY"] = access_df["Secret access key"][0]
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"


session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_DEFAULT_REGION"]
)
bedrock_runtime = session.client("bedrock-runtime", region_name="us-west-2")

def demo_chatbot():
    demo_llm=ChatBedrock(
       model_id='anthropic.claude-3-sonnet-20240229-v1:0',
       client=bedrock_runtime,
       model_kwargs= {
           "max_tokens": 300,
           "temperature": 0.1,
           "top_p": 0.9,
           "stop_sequences": ["\n\nHuman:"]} )
    return demo_llm


def demo_memory():
    llm_data=demo_chatbot()
    memory=ConversationSummaryBufferMemory(llm=llm_data,max_token_limit=300)
    return memory

def demo_conversation(input_text,memory):
    llm_chain_data=demo_chatbot()
    llm_conversation=ConversationChain(llm=llm_chain_data,memory=memory,verbose=True)

    chat_reply=llm_conversation.invoke(input_text)
    return chat_reply['response']
