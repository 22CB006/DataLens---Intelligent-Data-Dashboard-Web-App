"""
Custom Exception Classes

This module defines custom exceptions with user-friendly error messages.
"""

from fastapi import HTTPException, status


class DataLensException(HTTPException):
    """Base exception for DataLens application."""
    
    def __init__(self, status_code: int, detail: str, user_message: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.user_message = user_message or detail


# Authentication Exceptions
class InvalidCredentialsError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            user_message="The email or password you entered is incorrect. Please try again."
        )


class TokenExpiredError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            user_message="Your session has expired. Please log in again."
        )


class InvalidTokenError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            user_message="Invalid authentication. Please log in again."
        )


class UserNotFoundError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            user_message="The requested user could not be found."
        )


class UserAlreadyExistsError(DataLensException):
    def __init__(self, field: str = "email"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this {field} already exists",
            user_message=f"An account with this {field} already exists. Please use a different {field} or log in."
        )


class InactiveUserError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
            user_message="Your account has been deactivated. Please contact support."
        )


# Dataset Exceptions
class DatasetNotFoundError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
            user_message="The requested dataset could not be found. It may have been deleted."
        )


class DatasetAccessDeniedError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this dataset",
            user_message="You don't have permission to access this dataset."
        )


class InvalidFileTypeError(DataLensException):
    def __init__(self, allowed_types: list):
        types_str = ", ".join(allowed_types)
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {types_str}",
            user_message=f"Please upload a valid file. Supported formats: {types_str}"
        )


class FileTooLargeError(DataLensException):
    def __init__(self, max_size_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB",
            user_message=f"The file is too large. Maximum file size is {max_size_mb}MB."
        )


class FileProcessingError(DataLensException):
    def __init__(self, reason: str = None):
        detail = f"Error processing file: {reason}" if reason else "Error processing file"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            user_message="We couldn't process your file. Please make sure it's a valid CSV, Excel, or JSON file."
        )


class EmptyDatasetError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dataset is empty",
            user_message="The uploaded file is empty or contains no data."
        )


# Analysis Exceptions
class InsufficientDataError(DataLensException):
    def __init__(self, operation: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient data for {operation}",
            user_message=f"There isn't enough data to perform {operation}. Please upload a larger dataset."
        )


class InvalidColumnError(DataLensException):
    def __init__(self, column_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column '{column_name}' not found in dataset",
            user_message=f"The column '{column_name}' doesn't exist in your dataset."
        )


class NoNumericColumnsError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No numeric columns found in dataset",
            user_message="Your dataset doesn't contain any numeric columns for analysis."
        )


# Validation Exceptions
class ValidationError(DataLensException):
    def __init__(self, field: str, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error for field '{field}': {message}",
            user_message=f"Invalid {field}: {message}"
        )


# General Exceptions
class DatabaseError(DataLensException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
            user_message="Something went wrong. Please try again later."
        )


class ServerError(DataLensException):
    def __init__(self, message: str = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message or "Internal server error",
            user_message="Something went wrong on our end. Please try again later."
        )
