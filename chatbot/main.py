from fastapi import FastAPI

# create an object "app" to handle all requests
app = FastAPI()

# root url "/" visited, run this function (127.0.0.1:8000/)
@app.get("/")
def read_root():
    print("chatbot api backend is running")
    return {"message":"chatbot api backend is running"}

