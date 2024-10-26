from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
@app.get("/")
async def hello():
    return {"message": "hello world!"}