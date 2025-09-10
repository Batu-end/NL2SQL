from fastapi import FastAPI
from pydantic import BaseModel # FastAPI utilizes pydantic library to validate incoming data format
from agent import generate_response

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


# gets only packages containing POST requests. not GET.
@app.post("/api/ask")
def question_asked(request: Question):

    user_question = request.question

    print(f"Received question: {user_question}")

    try:
        final_answer = generate_response(user_question)
        return final_answer
    except Exception as e:
        print(f"Error occured: {e}")