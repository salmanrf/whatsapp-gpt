
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def getHealthCheck():
    return "I am healthy"
