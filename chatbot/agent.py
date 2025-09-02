from strands import Agent
import boto3    # AWS's SDK services for Python

bedrock_client = boto3.client(
    ServiceName='bedrock-runtime', 
    RegionName='us-west-2'     # Oregon, since California doesn't have access to Bedrock
)

