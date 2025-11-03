# Agentic NL2SQL Chatbot

This project is an Agentic AI chatbot that removes technical barriers from data access and retrieval by allowing users to use plain English prompts, such as "Give me the percentage of red cars."
The complex part, the syntax, is handled by the agent afterwards, where the agent transforms the natural language prompt into a complex SQL query. After the query is ran in the database, the answer is also displayed back in English.

The testing dataset were cars, which is why the examples will be car-related.

## 🚀 Key Features

* **Natural Language to SQL:** Translates plain English questions (e.g., "How many red cars are there?") into precise PostgreSQL queries.
* **Agentic Framework:** Uses a Strands Agent to manage the AI model, its tools, and the conversational flow.
* **Real-Time Data:** Connects directly to a live AWS RDS database, ensuring answers are always up-to-date.
* **Secure:** All database credentials are securely managed using AWS Secrets Manager.
* **Scalable:** Designed to be deployed on AWS App Runner, providing a scalable, serverless backend.
* **Conversational Memory:** The agent remembers the context of the conversation up to 10 messages to answer follow-up questions.

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | **Python 3.11**, **FastAPI** | API backkend. |
| **Server** | **Uvicorn** | Serves the FastAPI application in production. |
| **AI Agent** | **Strands Agents** | Manages the core AI logic and tool use. |
| **AI Model** | **Amazon Bedrock (Claude Haiku 3.5)** | Provides the reasoning and language understanding. |
| **Tooling** | **Strands Tools (`@tool`)** | Defines custom tools for the agent. |
| **Database** | **PostgreSQL (AWS RDS)** | The structured relational database we are querying. |
| **DB Driver** | **psycopg2** | The Python library for connecting to PostgreSQL. |
| **Cloud Hosting**| **AWS App Runner** | Runs the backend service in a serverless container. |
| **Security** | **AWS Secrets Manager**, **IAM** | Secures database credentials and service permissions. |
| **Frontend** | **React** | The user interface. Can be found at the [frontend repository](https://github.com/Batu-end/NL2SQL-front) |

---

## 🏛️ Architecture

The application follows a standard architecture, orchestrated by the AI agent.

1.  **Frontend (React):** The user sends a question from the React/web app.
2.  **API Backend (FastAPI on App Runner):** The FastAPI server receives the request at the endpoint.
3.  **Agent (`agent.py`):** The API calls the `get_chatbot_response` function. This function:
    * Builds a prompt containing the user's question, conversation history, and the database schema.
    * Initializes a Strands `Agent`.
    * Tells the agent to use the custom `@tool` named `execute_sql`.
4.  **AI Model (Bedrock):** The agent sends the prompt to the AI model on Amazon Bedrock. The current model we used for testing was Anthropic's Claude Haiku 3.5 The model determines it needs to use the tool and generates the necessary SQL query.
5.  **Tool Execution:** The agent calls the tool, which in turn runs the query itself.
6.  **Security (Secrets Manager):** The agent first fetches the database credentials securely from AWS Secrets Manager.
7.  **Database (RDS):** Connects to the PostgreSQL database on AWS RDS and executes the AI-generated query.
8.  **Response:** The query result is passed back to the agent. The agent sends this result to Bedrock, which formats it into a human-friendly answer (e.g., "There are 2 red cars."). This final answer is sent back to the user's frontend.

---

## ⚙️ Getting Started (Local Development)

### Prerequisites

* Python 3.11
* An AWS account with access to Bedrock, RDS, and Secrets Manager
* AWS CLI installed and configured (`aws configure`)
* A running PostgreSQL database (Local also works, we used RDS)

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/YourRepo.git](https://github.com/YourUsername/YourRepo.git)
cd YourRepo
```

### 2. Environment
# Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
