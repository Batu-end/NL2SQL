from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # FastAPI utilizes pydantic library to validate incoming data format
from agent import generate_response

# create an object "app" to handle all requests
app = FastAPI()

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
async def question_asked(request: Question):

    user_question = request.question

    print(f"Received question: {user_question}")

    try:
        final_answer = await generate_response(user_question)
        print('Final answer:', final_answer)
        return {"answer": final_answer}
    except Exception as e:
        print(f"Error occured: {e}")