import json
import psycopg2     # PostgreSQL database handler library for Python
import boto3
from botocore.exceptions import ClientError

# fetch password from Secrets Manager. straight from AWS guide.
def get_secret():

    """Fetches database credentials from AWS Secrets Manager."""
    secret_name = "Ver2"
    region_name = "us-west-2"

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

    secret = json.loads(get_secret_value_response['SecretString'])

    return secret


# function to run the SQL query from prompt.
# from the Psycopg2 documentation: https://www.psycopg.org/docs/usage.html
def run_query(query: str):
    """Connects to database and runs SQL query"""

    conn = None

    try:
        creds = get_secret()
        
        conn = psycopg2.connect(database='postgres',
                                user='postgres',
                                password=creds['password'],
                                host='postgres.cp0ec0oi4dp9.us-west-2.rds.amazonaws.com',
                                port='5432')
        

        cursor = conn.cursor()
        cursor.execute(query)

        if cursor.description:
            result = cursor.fetchall()
        else:
            result = "!! QUERY SUCCESSFUL !!"

        print(f"--- DATABASE: Query returned: {result} ---") # see what db returns

        cursor.close()
        return result
    
    except Exception as e:
        print(f"!! DATABASE CONNECTION ERROR: {e} !!")
        return None
    finally:
        if conn is not None:
            conn.close()
            print("--- DATABASE: Connection closed. ---")
