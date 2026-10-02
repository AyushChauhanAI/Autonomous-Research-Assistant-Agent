from fastapi import FastAPI
from routers.generate import router

app = FastAPI()

app.include_router(router)