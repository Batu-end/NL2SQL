import psycopg2     # PostgreSQL database handler library for Python
import boto3
from botocore.exceptions import ClientError

host_name = "database-1.cp0ec0oi4dp9.us-west-2.rds.amazonaws.com"
user_name = "postgres"
port = "5432"

# fetch password from Secrets Manager
def get_secret():

    secret_name = "nl2sql/initialdb"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    # Your code goes here.


query = str

# function to run the SQL query from prompt
# 
def run_query(query):












# # --- IMPORTANT ---
# # For now, we will hardcode credentials. We will replace this with
# # AWS Secrets Manager later.
# DB_NAME = "your_db_name"
# DB_USER = "your_username"
# DB_PASSWORD = "your_password"
# DB_HOST = "localhost" # This will be your RDS endpoint later
# DB_PORT = "5432"

# def run_query(query: str):
#     """Connects to the database and runs a given SQL query."""
#     try:
#         conn = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         cursor = conn.cursor()
#         cursor.execute(query)
#         # For now, let's assume the query returns results
#         result = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return result
#     except Exception as e:
#         print(f"Database error: {e}")
#         return None