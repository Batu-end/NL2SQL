from strands import Agent
import boto3    # AWS's SDK services for Python
from database import run_query

bedrock_client = boto3.client(
    ServiceName='bedrock-runtime', 
    RegionName='us-west-2'     # Oregon, since California doesn't have access to Bedrock
)

def execute_sql(sql_query: str) -> str:
    """
    Executes SQL query and returns a string by calling run_query function.
    Use this tool to answer questions or get information from the databse.
    """

    print(f"Executing query: {sql_query}")

    result = run_query(sql_query)

    return str(result)