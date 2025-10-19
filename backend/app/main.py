"""
Main FastAPI Application

This is the entry point of our backend application.

What you'll learn:
- FastAPI application initialization
- CORS middleware configuration
- API routing
- Application lifecycle events
- Auto-generated API documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent Data Dashboard Web Application API",
    docs_url="/docs",  # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",  # ReDoc at http://localhost:8000/redoc
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows our frontend (running on different port) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Frontend URLs
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Root endpoint - Health check
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Returns API status.
    
    This is useful for:
    - Health checks
    - Verifying API is running
    - Load balancer health checks
    """
    return {
        "message": "Welcome to DataLens API",
        "status": "online",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the application.
    Used by monitoring tools and load balancers.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Application startup event
@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    
    Use this for:
    - Database connection initialization
    - Cache warming
    - Loading ML models
    - Any one-time setup tasks
    """
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Debug mode: {settings.DEBUG}")


# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    
    Use this for:
    - Closing database connections
    - Cleaning up resources
    - Saving state
    """
    print(f"👋 {settings.APP_NAME} shutting down...")


# Import API routers
from app.api import auth, users, datasets, analysis

# Include API routers with versioning
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    datasets.router,
    prefix="/api/v1/datasets",
    tags=["Datasets"]
)

app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["Analysis"]
)


# What's happening here?
# ----------------------
# 1. We create a FastAPI instance with configuration
# 2. We add CORS middleware to allow frontend access
# 3. We define basic endpoints (/, /health)
# 4. We set up startup/shutdown events
# 5. Later, we'll add API routers for different features
#
# How to run:
# uvicorn app.main:app --reload
#
# Then visit:
# - http://localhost:8000 - Root endpoint
# - http://localhost:8000/docs - Interactive API docs (Swagger UI)
# - http://localhost:8000/redoc - Alternative API docs (ReDoc)
