# from strands import Agent
# import boto3    # AWS's SDK services for Python
# from database import run_query
# from strands.models.anthropic import AnthropicModel

# bedrock_client = boto3.client(
#     service_name='bedrock-runtime', 
#     region_name='us-west-2'     # Oregon, since California doesn't have access to Bedrock
# )

# # allows agent to interact with database
# def execute_sql(sql_query: str) -> str:
#     """
#     Executes SQL query and returns a string by calling run_query function.
#     Use this tool to answer questions or get information from the databse.
#     """

#     print(f"Executing query: {sql_query}")

#     result = run_query(sql_query)

#     return str(result)

# # 
# def generate_response(user_prompt: str) -> str:

#     schema = """
#     CREATE TABLE cars (
#         id SERIAL PRIMARY KEY,
#         make VARCHAR(50) NOT NULL,
#         model VARCHAR(50) NOT NULL,
#         year INT,
#         price INT,
#         color VARCHAR(30)
#     );
#     """

#     full_prompt = f"""
#     You are an expert PostgreSQL analyst. Based on the schema below, your task is to answer the user's question.
#     1. First, you must write a single, syntactically correct PostgreSQL query.
#     2. Second, you must use the 'execute_sql' tool to run that query.
#     3. Finally, based on the results from the tool, answer the user's question in a clear, friendly sentence. Do not show the SQL query in your final answer.

#     Schema: {schema}

#     My Question: {user_prompt}
#     """

#     model = AnthropicModel(

#         # **model_config
#         max_tokens=512,
#         model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
#         params={
#             "temperature": 0.7,
#         }
#     )

#     agent = Agent(model=
#                   model, 
#                   tools=[execute_sql],
#                   client=bedrock_client)
#     response = agent(full_prompt)
#     print(response)
#     return response

# if __name__ == "__main__":
#     test_question = "List the make, model, and year of all cars."
#     print(f"Testing with question: '{test_question}'")
#     print("-" * 20)
    
#     response = generate_response(test_question)
    
#     print("-" * 20)
#     print(f"✅ Final Answer: {response}")