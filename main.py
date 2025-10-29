from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from controllers.home_controller import HomeController
from controllers.auth_controller import AuthController
from controllers.recognition_controller import RecognitionController
from controllers.training_controller import TrainingController
from exceptions.custom_exception import CustomException
from core.exception_handler import obe_exception_handler
from core.logger import get_daily_logger

# --------------------------------------------------
# Logger
# --------------------------------------------------
logger = get_daily_logger()

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="Recognition Beef API",
    description="API for recognizing beef using deep learning models",
    version="1.0",
)

# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------
origins = [
    "*",  # Allow all origins (not recommended for production)
    # "http://localhost:5173",  # Example for React
    # "http://127.0.0.1:5173",  # Alternative for React
    # "http://localhost:3000",  # Example for Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # or specify: ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],   # or specify allowed headers
)

# --------------------------------------------------
# Middleware - Logging
# --------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    # Log only errors (status >= 400)
    if response.status_code >= 400:
        logger.error(
            f"ERROR {response.status_code} | {request.method} {request.url} | "
            f"AGENT: {request.client.host} - {request.headers.get('user-agent')}"
        )

    return response

# --------------------------------------------------
# Exception Handlers
# --------------------------------------------------
app.add_exception_handler(CustomException, obe_exception_handler)
# app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
# app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)

# --------------------------------------------------
# API Routes
# --------------------------------------------------
API_PREFIX = "/api"

# Home Routes
home_controller = HomeController()
app.include_router(home_controller.router, prefix=API_PREFIX)

# Auth Routes
auth_controller = AuthController()
app.include_router(auth_controller.router, prefix=API_PREFIX)

# Recognition Routes
recognition_controller = RecognitionController()
app.include_router(recognition_controller.public_router, prefix=API_PREFIX)

# Training Routes
training_controller = TrainingController()
app.include_router(training_controller.router, prefix=API_PREFIX)
