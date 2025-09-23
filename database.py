import json
import psycopg2     # PostgreSQL database handler library for Python
import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine

# --- SQLAlchemy Engine Setup ---
# This will be imported by the FastAPI app for schema and data browsing.
engine = None

def get_secret():
    """Fetches database credentials from AWS Secrets Manager."""
    secret_name = "Ver2"
    region_name = "us-west-2"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret
    except ClientError as e:
        print(f"FATAL: Could not fetch secrets from AWS Secrets Manager. Error: {e}")
        raise e

try:
    creds = get_secret()
    # Format: "postgresql://<user>:<password>@<host>:<port>/<dbname>"
    DATABASE_URL = (
        f"postgresql://postgres:{creds['password']}"
        f"@postgres.cp0ec0oi4dp9.us-west-2.rds.amazonaws.com:5432/postgres"
    )
    engine = create_engine(DATABASE_URL)
    # Test the connection
    with engine.connect() as connection:
        print("Successfully connected to the database via SQLAlchemy.")
except Exception as e:
    print(f"FATAL: Error creating database engine. API endpoints for schema/data browsing will not work.")
    print(f"Error details: {e}")
    # If engine creation fails, it remains None. The API will gracefully handle this.

# --- Original Query Function (for the agent) ---
# This remains unchanged for the agent's use.
def run_query(query: str):
    """Connects to database and runs SQL query (used by the agent)."""
    conn = None
    try:
        creds = get_secret()
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password=creds['password'],
            host='postgres.cp0ec0oi4dp9.us-west-2.rds.amazonaws.com',
            port='5432'
        )
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description:
            result = cursor.fetchall()
        else:
            result = "!! QUERY SUCCESSFUL !!"
        print(f"--- DATABASE: Query returned: {result} ---")
        cursor.close()
        return result
    except Exception as e:
        print(f"!! DATABASE CONNECTION ERROR: {e} !!")
        return None
    finally:
        if conn is not None:
            conn.close()
            print("--- DATABASE: Connection closed. ---")
