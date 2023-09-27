from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import uuid
import whisper
import os
from dotenv import load_dotenv

load_dotenv()

api_keys = os.environ['API_KEYS'].split(',')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI()


@app.post("/transcribe", dependencies=[Depends(api_key_auth)])
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
