from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, notes, todos

app = FastAPI(
    title="Notes & Todos API",
    description="A FastAPI application with JWT auth, RBAC, and organization-based data sharing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server (CRA & Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])

@app.get("/")
async def root():
    return {"message": "Welcome to Notes & Todos API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}