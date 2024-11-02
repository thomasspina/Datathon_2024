import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

access_df = pd.read_csv(r"C:\Users\user\OneDrive\Documents\Polytechnique\A24\Datathon\Datathon_2024\amazon-bedrock-agent-test-ui-main\admin_accessKeys.csv")
os.environ["AWS_ACCESS_KEY_ID"] = access_df["Access key ID"][0]
os.environ["AWS_SECRET_ACCESS_KEY"] = access_df["Secret access key"][0]
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

def invoke_agent(agent_id, agent_alias_id, session_id, prompt):
    try:

        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ["AWS_DEFAULT_REGION"]
            )
        bedrock_runtime = session.client("bedrock-agent-runtime", region_name="us-west-2")
        # See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html
        response = bedrock_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            enableTrace=True,
            sessionId=session_id,
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
                for trace_type in ["guardrailTrace", "preProcessingTrace", "orchestrationTrace", "postProcessingTrace"]:
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
                        trace[mapped_trace_type].append(event["trace"]["trace"][trace_type])

    except ClientError as e:
        raise

    return {
        "output_text": output_text,
        "citations": citations,
        "trace": trace
    }
