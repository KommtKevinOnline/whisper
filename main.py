from fastapi import FastAPI, Request
import uuid
import whisper
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


@app.post("/transcribe")
async def transcibe(request: Request):
    data: bytes = await request.body()

    file_name = '%s.mp4a' % uuid.uuid4()

    f = open(file_name, "wb")
    f.write(data)
    f.close()

    model = whisper.load_model("base")

    result = model.transcribe(file_name)

    os.remove(file_name)

    return result
