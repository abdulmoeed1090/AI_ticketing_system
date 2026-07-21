from fastapi import FastAPI


from src.middleware.logger import log_requests

from src.routers import (
    auth,
    ticket,
    chat,
    admin
)

app = FastAPI(
    title="AI Support Ticket System",
    description="Backend Learning Project using FastAPI, PostgreSQL, JWT, RBAC and Gemini AI",
    version="1.0.0"
)

# -------------------------
# Middleware
# -------------------------
app.middleware("http")(log_requests)


# -------------------------
# Routers
# -------------------------
app.include_router(auth.router)
app.include_router(ticket.router)
app.include_router(chat.router)
app.include_router(admin.router)


@app.get("/")
def home():
    return {
        "message": "AI Support Ticket System API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }