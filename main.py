from fastapi import FastAPI
import uvicorn
from router.router import user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(user_router)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":  
    uvicorn.run("main:app", host="0.0.0.0", port=8083)
