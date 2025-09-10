from fastapi import FastAPI
from pydantic import BaseModel # FastAPI utilizes pydantic library to validate incoming data format


# create an object "app" to handle all requests
app = FastAPI()

# root url "/" visited, run this function (127.0.0.1:8000/)
@app.get("/")
def read_root():
    print("chatbot api backend is running")
    return {"message":"chatbot api backend is running"}


# the class to define the structure of the type of data we expect to receive from the user
# the API will expect something like a JSON file {"question": "string"}
class Question(BaseModel):
    question: str


#########
## WIP ##
#########

# gets only packages containing POST requests. not GET.
@app.post("/api/ask")
def question_asked(request: Question):

    user_question = request.question

    print(f"Received question: {user_question}")

    # return JSON to confirm for now
    return {
        "request_status": "success",
        "hardcoded_answer": "hardcoded response for Toyota Camry",
        "data": [{"id": 1, "make": "Toyota", "model": "Camry", "year": 2020, "price": "20000", "color": "blue"}],
        "query": "SELECT * FROM cars WHERE model = 'Camry';",
        "user_request": user_question
    }


