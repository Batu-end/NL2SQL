from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from typing import List, Dict, Any

# Use SQLAlchemy for schema/data browsing, and the agent for NL2SQL
from sqlalchemy import inspect, text
from agent import generate_response
from database import engine  # Import the configured SQLAlchemy engine

# create an object "app" to handle all requests
app = FastAPI(
    title="NL2SQL Backend API",
    description="API for fetching database schema, data, and answering natural language questions.",
    version="1.1.0",
)

# --- CORS (Cross-Origin Resource Sharing) ---
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models (Data Shapes) ---

# For the NL2SQL agent
class Question(BaseModel):
    question: str
    session_id: str | None = None

# For the schema/data browsing API
class Database(BaseModel):
    value: str
    label: str

class ColumnSchema(BaseModel):
    name: str
    type: str

class ForeignKey(BaseModel):
    column: str
    references: str
    on: str

class TableSchema(BaseModel):
    name: str
    columns: List[ColumnSchema]
    foreignKeys: List[ForeignKey] = []

class PaginatedDataResponse(BaseModel):
    rows: List[Dict[str, Any]]
    totalRows: int


# --- API Endpoints ---

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    print("NL2SQL API backend is running")
    return {"message": "NL2SQL API backend is running"}

# --- Agent Endpoint ---

@app.post("/api/ask")
async def question_asked(request: Question):
    """Endpoint for the NL2SQL agent."""
    user_question = request.question
    session_id = request.session_id or str(uuid4())
    print(f"Received question (session {session_id}): {user_question}")
    try:
        final_answer = await generate_response(user_question, session_id=session_id)
        print('Final answer:', final_answer)
        return {"answer": final_answer, "session_id": session_id}
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Schema and Data Browsing Endpoints ---

@app.get("/api/databases", response_model=List[Database])
def get_databases():
    """
    Returns a list of available databases.
    For this implementation, we assume a single, primary database.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Database is not configured or connection failed.")
    return [{"value": "default_db", "label": "Primary Database"}]


@app.get("/api/schema/{db_name}", response_model=List[TableSchema])
def get_schema(db_name: str):
    """
    Inspects the database and returns the schema for all tables.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Database is not configured or connection failed.")
    try:
        inspector = inspect(engine)
        schema_data = []
        table_names = inspector.get_table_names()
        for table_name in table_names:
            columns = inspector.get_columns(table_name)
            fks = inspector.get_foreign_keys(table_name)
            table_schema = TableSchema(
                name=table_name,
                columns=[ColumnSchema(name=c["name"], type=str(c["type"])) for c in columns],
                foreignKeys=[
                    ForeignKey(
                        column=fk["constrained_columns"][0],
                        references=fk["referred_table"],
                        on=fk["referred_columns"][0],
                    )
                    for fk in fks
                ],
            )
            schema_data.append(table_schema)
        return schema_data
    except Exception as e:
        print(f"Error fetching schema: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the database schema.")


@app.get("/api/data/{table_name}", response_model=PaginatedDataResponse)
def get_table_data(table_name: str, page: int = 1, limit: int = 10):
    """
    Fetches paginated data from a specific table.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Database is not configured or connection failed.")
    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")
        
        offset = (page - 1) * limit
        with engine.connect() as connection:
            count_query = text(f'SELECT COUNT(*) FROM "{table_name}"')
            total_rows_result = connection.execute(count_query).scalar_one()
            
            data_query = text(f'SELECT * FROM "{table_name}" LIMIT :limit OFFSET :offset')
            result = connection.execute(data_query, {"limit": limit, "offset": offset})
            
            rows = [dict(row._mapping) for row in result]
            return {"rows": rows, "totalRows": total_rows_result}
    except Exception as e:
        print(f"Error fetching data for table '{table_name}': {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching data for table '{table_name}'.")
