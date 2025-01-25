from fastapi import FastAPI
from router.router  import user_router

app = FastAPI()

app.include_router(user_router)