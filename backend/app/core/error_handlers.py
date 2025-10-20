"""
Global Error Handlers

This module provides global exception handlers for the FastAPI application.
All errors are formatted with user-friendly messages for frontend display.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors with user-friendly messages.
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message
        })
    
    # Create user-friendly message
    if len(errors) == 1:
        user_message = f"Invalid {errors[0]['field']}: {errors[0]['message']}"
    else:
        user_message = "Please check your input and try again."
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "user_message": user_message,
            "errors": errors
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (e.g., unique constraint violations).
    """
    error_message = str(exc.orig)
    
    # Parse common integrity errors
    if "unique constraint" in error_message.lower():
        if "email" in error_message.lower():
            user_message = "An account with this email already exists."
        elif "username" in error_message.lower():
            user_message = "This username is already taken."
        elif "filename" in error_message.lower():
            user_message = "A dataset with this name already exists."
        else:
            user_message = "This record already exists."
    elif "foreign key constraint" in error_message.lower():
        user_message = "Cannot complete this action due to related data."
    elif "not null constraint" in error_message.lower():
        user_message = "Required information is missing."
    else:
        user_message = "Database error occurred. Please try again."
    
    logger.error(f"Integrity error: {error_message}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity error",
            "user_message": user_message
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle general SQLAlchemy database errors.
    """
    logger.error(f"Database error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error",
            "user_message": "A database error occurred. Please try again later."
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all other unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "user_message": "Something went wrong. Please try again later."
        }
    )


def add_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)
