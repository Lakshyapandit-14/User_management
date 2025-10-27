from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user.v1 import router as user_router
from app.api.auth.v1 import router as auth_router
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.connections.database import engine, Base
from app.api.user.v1 import profile_router

# Create FastAPI app
app = FastAPI(
    title="User Management Microservice",
    description="A modular FastAPI-based user management service with authentication and authorization.",
    version="1.0.0",
)

# Enable CORS (Cross-Origin Resource Sharing)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # You can restrict this later to your frontend domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
 # now (19/10/2025 : 9:33 am)
# Include versioned routers
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
#app.include_router(profile_router, prefix="/api/v1/user", tags=["Profile"])

# Health check endpoint
@app.get("/", tags=["Demo"])
def health_check():
    return {"status": "ok", "message": "User Management Microservice is running 🚀"}

# Run app (for direct execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)