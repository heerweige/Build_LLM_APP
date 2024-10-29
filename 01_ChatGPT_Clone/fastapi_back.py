from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

client = OpenAI(
    api_key='sk-4ab55d5516414bdb97a6a53b823f0dde',  # 这里可以替换为 os.getenv("DASHSCOPE_API_KEY") 如果使用环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

app = FastAPI()

class Item(BaseModel):
    role: str
    content: str

class ReqestIntputs(BaseModel):
    model: str
    messages: list[Item]

def openai_response(model, messages):
    chat_response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    reply = chat_response.choices[0].message.content
    return reply

@app.post("/openai")
async def openai_AI(reqest_intputs: ReqestIntputs):
    try:
        reply = openai_response(reqest_intputs.model, reqest_intputs.messages)
        return {"content": reply}
    except Exception as e:
        return {"error": str(e)}

