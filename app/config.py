import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
    AGENT_ID = os.getenv("AGENT_ID")
    AGENT_ALIAS_ID = os.getenv("AGENT_ALIAS_ID")
