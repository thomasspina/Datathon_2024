import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd
from config import Config
from typing import Dict, Any, List


class BedrockAgent:
    def __init__(self):
        """Initialize the BedrockAgent instance with None values."""
        self.session = None
        self.bedrock_runtime = None
        self.agent_id = None
        self.agent_alias_id = None

    def initialize_session(self):
        """Initialize the BedrockAgent with AWS credentials and agent details."""
        self.session = boto3.Session(
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION,
        )
        self.bedrock_runtime = self.session.client(
            "bedrock-agent-runtime", region_name="us-west-2"
        )
        self.agent_id = Config.AGENT_ID
        self.agent_alias_id = Config.AGENT_ALIAS_ID

    def invoke_agent(self, session_id: str, prompt: str) -> Dict[str, Any]:
        """
        Invokes the Bedrock agent and returns the response including output text, citations, and trace information.

        :param session_id: Session identifier
        :param prompt: The input prompt for the agent
        :return: A dictionary containing the output text, citations, and trace information
        """
        try:
            response = self.bedrock_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                enableTrace=True,
                sessionId=session_id,
                inputText=prompt,
            )

            output_text, citations, trace = self._parse_response(response)
            return {"output_text": output_text, "citations": citations, "trace": trace}

        except ClientError as e:
            raise RuntimeError(f"Failed to invoke agent: {e}")

    def _parse_response(
        self, response: Dict[str, Any]
    ) -> (str, List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]):
        """
        Parses the response from Bedrock, extracting the output text, citations, and trace details.

        :param response: The response dictionary from the agent invocation
        :return: Tuple of output text, citations, and trace data
        """
        output_text = ""
        citations = []
        trace = {}
        has_guardrail_trace = False

        for event in response.get("completion", []):
            # Extract output text chunks
            if "chunk" in event:
                chunk = event["chunk"]
                output_text += chunk["bytes"].decode()
                if "attribution" in chunk:
                    citations.extend(chunk["attribution"].get("citations", []))

            # Extract trace information
            # if "trace" in event:
            #     trace = self._extract_trace(event, trace, has_guardrail_trace)

        return output_text, citations, trace

    # def _extract_trace(
    #     self,
    #     event: Dict[str, Any],
    #     trace: Dict[str, List[Dict[str, Any]]],
    #     has_guardrail_trace: bool,
    # ) -> Dict[str, List[Dict[str, Any]]]:
    #     """
    #     Helper method to extract and organize trace data.

    #     :param event: Individual event dictionary in the response
    #     :param trace: Dictionary to accumulate trace information
    #     :param has_guardrail_trace: Boolean flag to manage guardrail trace handling
    #     :return: Updated trace dictionary with organized trace data
    #     """
    #     for trace_type in [
    #         "guardrailTrace",
    #         "preProcessingTrace",
    #         "orchestrationTrace",
    #         "postProcessingTrace",
    #     ]:
    #         if trace_type in event["trace"]["trace"]:
    #             mapped_trace_type = trace_type
    #             if trace_type == "guardrailTrace":
    #                 if not has_guardrail_trace:
    #                     has_guardrail_trace = True
    #                     mapped_trace_type = "preGuardrailTrace"
    #                 else:
    #                     mapped_trace_type = "postGuardrailTrace"
    #             trace.setdefault(mapped_trace_type, []).append(
    #                 event["trace"]["trace"][trace_type]
    #             )
    #     return trace
