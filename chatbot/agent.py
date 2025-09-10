from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool
from database import run_query


# allows agent to interact with database
@tool
def execute_sql(sql_query: str) -> str:
    """
    Executes SQL query and returns a string by calling run_query function.
    Use this tool to answer questions or get information from the databse.
    """

    print(f"Executing query: {sql_query}")

    result = run_query(sql_query)

    print(f"--- AGENT: Received from database: {result} ---") # see what agent receives
    return str(result)

# 
def generate_response(user_prompt: str) -> str:

    schema = """
    CREATE TABLE cars (
        id SERIAL PRIMARY KEY,
        make VARCHAR(50) NOT NULL,
        model VARCHAR(50) NOT NULL,
        year INT,
        price INT,
        color VARCHAR(30)
    );
    """

    full_prompt = f"""
    You are an expert PostgreSQL analyst. Based on the schema below, your task is to answer the user's question.
    1. First, you must write a single, syntactically correct PostgreSQL query.
    2. Second, you must use the 'execute_sql' tool to run that query.
    3. Based on the results from the tool, answer the user's question in a clear, friendly sentence. Do not show the SQL query in your final answer.
    4. Finally, always double check, and make sure you don't hallucinate.

    Schema: {schema}

    My Question: {user_prompt}
    """

    model = BedrockModel(

        # **model_config
        max_tokens=512,
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        config={"region_name": "us-west-2"}
    )

    agent = Agent(
        model=model,
        tools=[execute_sql],
    )

    response = agent(full_prompt)
    final_text = response # will add indexing to receive only the true response later
    # print(response)
    return final_text