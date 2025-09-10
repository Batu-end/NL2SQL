from database import run_query

# small sandbox to see if database connection is working
def test_database_connection():
    print("Attempting to connect to the database and run a query...")
    
    # A simple, safe query to test the connection
    test_query = "SELECT make, model FROM cars LIMIT 3;"
    
    results = run_query(test_query)
    
    if results is not None:
        print("\n✅ Connection successful!")
        print("Query results:")
        for row in results:
            print(f"- Make: {row[0]}, Model: {row[1]}")
    else:
        print("\n❌ Connection failed. Check the error messages above.")

# This makes the script runnable from the command line
if __name__ == "__main__":
    test_database_connection()