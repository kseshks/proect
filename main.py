from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import auth, admin, teacher, student


app = FastAPI(
    title="Education AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(student.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}