from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from src.summary import respond_to_context 

from src.utility import handle_response

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    title: str
    prompt: str


@app.post("/summary")
async def get_message(item: Item):

    new_title = item.title
    prompt = str(item.prompt)
    print(type(new_title))
    try:
        answer = respond_to_context(question=new_title, input_prompt=prompt)
    except Exception as error:
        return handle_response(code=400, message=f"error {error}", data="")

    if not answer:

        return handle_response(code=400, message="error with OpenAI api", data="")

    return handle_response(code=200, message="", data=answer)

