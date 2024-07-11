from fastapi import FastAPI
from routers import client_routers

app = FastAPI()
app.include_router(client_routers.router)