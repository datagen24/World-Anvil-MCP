"""Shared fixtures for endpoint tests.

This module provides fixtures specific to testing API endpoint implementations.
"""

import pytest


@pytest.fixture
def mock_response_success() -> dict:
    """Provide mock successful API response structure.

    Returns:
        dict: Generic successful response with success flag.
    """
    return {"success": True, "data": {}}


@pytest.fixture
def mock_response_error() -> dict:
    """Provide mock error API response structure.

    Returns:
        dict: Generic error response with success flag and error message.
    """
    return {"success": False, "error": "Test error message"}
