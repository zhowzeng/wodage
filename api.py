from loguru import logger
from agents import Agent, Runner, TResponseInputItem
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: list[TResponseInputItem]
    model: str


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chat API!"}


@app.post("/chat")
async def chat(request: ChatRequest):
    logger.debug(f"Received request: {request}")
    agent = Agent(
        name="General Assistant",
        instructions="回答使用者的問題，語言使用正體中文或英文。",
        model=request.model,
    )
    try:
        result = await Runner.run(agent, request.messages)
        result.raw_responses
        return {"response": result.final_output_as(str, raise_if_incorrect_type=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
