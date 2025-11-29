"""Tests for World Anvil API exception hierarchy.

Tests custom exception classes including:
- Exception hierarchy and inheritance
- Attribute initialization and validation
- Exception message formatting
- Status codes and retry-after values
"""

import pytest

from world_anvil_mcp.exceptions import (
    WorldAnvilAPIError,
    WorldAnvilAuthError,
    WorldAnvilError,
    WorldAnvilNotFoundError,
    WorldAnvilRateLimitError,
    WorldAnvilValidationError,
)


class TestWorldAnvilErrorBase:
    """Tests for WorldAnvilError base exception."""

    @pytest.mark.unit
    def test_base_error_instantiation(self) -> None:
        """Test creating WorldAnvilError with message."""
        # Act
        error = WorldAnvilError("Test error message")

        # Assert
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_base_error_without_message(self) -> None:
        """Test creating WorldAnvilError without message."""
        # Act
        error = WorldAnvilError()

        # Assert
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_base_error_inheritance(self) -> None:
        """Test WorldAnvilError is proper Exception subclass."""
        # Act
        error = WorldAnvilError("test")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, WorldAnvilError)


class TestWorldAnvilAuthError:
    """Tests for authentication/authorization error."""

    @pytest.mark.unit
    def test_auth_error_instantiation(self) -> None:
        """Test creating WorldAnvilAuthError."""
        # Act
        error = WorldAnvilAuthError("Authentication failed")

        # Assert
        assert str(error) == "Authentication failed"
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_auth_error_inheritance_chain(self) -> None:
        """Test AuthError follows proper inheritance chain."""
        # Act
        error = WorldAnvilAuthError("Auth failed")

        # Assert
        assert isinstance(error, WorldAnvilAuthError)
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_auth_error_catch_as_base(self) -> None:
        """Test AuthError can be caught as WorldAnvilError."""
        # Arrange
        error = WorldAnvilAuthError("Invalid credentials")

        # Act & Assert
        try:
            raise error
        except WorldAnvilError:
            pass  # Expected
        except Exception:
            pytest.fail("Should catch as WorldAnvilError")

    @pytest.mark.unit
    def test_auth_error_specific_messages(self) -> None:
        """Test AuthError with various error messages."""
        # Arrange
        messages = [
            "Invalid credentials",
            "User lacks permission",
            "Missing authentication headers",
            "Expired user token",
        ]

        # Act & Assert
        for msg in messages:
            error = WorldAnvilAuthError(msg)
            assert str(error) == msg


class TestWorldAnvilAPIError:
    """Tests for generic API error with status code."""

    @pytest.mark.unit
    def test_api_error_with_message_only(self) -> None:
        """Test WorldAnvilAPIError with message only."""
        # Act
        error = WorldAnvilAPIError("API error occurred")

        # Assert
        assert str(error) == "API error occurred"
        assert error.status_code is None
        assert isinstance(error, WorldAnvilError)

    @pytest.mark.unit
    def test_api_error_with_status_code(self) -> None:
        """Test WorldAnvilAPIError with message and status code."""
        # Act
        error = WorldAnvilAPIError("Bad request", status_code=400)

        # Assert
        assert str(error) == "Bad request"
        assert error.status_code == 400

    @pytest.mark.unit
    def test_api_error_with_various_status_codes(self) -> None:
        """Test WorldAnvilAPIError with different HTTP status codes."""
        # Arrange
        test_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (500, "Internal server error"),
            (502, "Bad gateway"),
            (503, "Service unavailable"),
        ]

        # Act & Assert
        for status_code, msg in test_cases:
            error = WorldAnvilAPIError(msg, status_code=status_code)
            assert error.status_code == status_code
            assert str(error) == msg

    @pytest.mark.unit
    def test_api_error_status_code_attribute(self) -> None:
        """Test status_code attribute is accessible."""
        # Act
        error = WorldAnvilAPIError("Error", status_code=500)

        # Assert
        assert hasattr(error, "status_code")
        assert error.status_code == 500

    @pytest.mark.unit
    def test_api_error_inheritance(self) -> None:
        """Test APIError proper inheritance chain."""
        # Act
        error = WorldAnvilAPIError("API error", status_code=400)

        # Assert
        assert isinstance(error, WorldAnvilAPIError)
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_api_error_catch_as_base(self) -> None:
        """Test APIError can be caught as WorldAnvilError."""
        # Arrange
        error = WorldAnvilAPIError("Server error", status_code=500)

        # Act & Assert
        try:
            raise error
        except WorldAnvilError:
            pass  # Expected
        except Exception:
            pytest.fail("Should catch as WorldAnvilError")

    @pytest.mark.unit
    def test_api_error_status_code_none_default(self) -> None:
        """Test APIError status_code defaults to None."""
        # Act
        error = WorldAnvilAPIError("No status code provided")

        # Assert
        assert error.status_code is None

    @pytest.mark.unit
    def test_api_error_with_zero_status_code(self) -> None:
        """Test APIError handles status_code=0."""
        # Act
        error = WorldAnvilAPIError("Zero status", status_code=0)

        # Assert
        assert error.status_code == 0

    @pytest.mark.unit
    def test_api_error_with_negative_status_code(self) -> None:
        """Test APIError accepts negative status codes."""
        # Act
        error = WorldAnvilAPIError("Negative status", status_code=-1)

        # Assert
        assert error.status_code == -1


class TestWorldAnvilRateLimitError:
    """Tests for rate limit exceeded error."""

    @pytest.mark.unit
    def test_rate_limit_error_with_message_only(self) -> None:
        """Test WorldAnvilRateLimitError with message only."""
        # Act
        error = WorldAnvilRateLimitError("Rate limit exceeded")

        # Assert
        assert str(error) == "Rate limit exceeded"
        assert error.retry_after == 60  # Default
        assert isinstance(error, WorldAnvilError)

    @pytest.mark.unit
    def test_rate_limit_error_with_retry_after(self) -> None:
        """Test WorldAnvilRateLimitError with custom retry_after."""
        # Act
        error = WorldAnvilRateLimitError("Rate limit", retry_after=120)

        # Assert
        assert str(error) == "Rate limit"
        assert error.retry_after == 120

    @pytest.mark.unit
    def test_rate_limit_error_retry_after_attribute(self) -> None:
        """Test retry_after attribute is accessible."""
        # Act
        error = WorldAnvilRateLimitError("Limited", retry_after=30)

        # Assert
        assert hasattr(error, "retry_after")
        assert error.retry_after == 30

    @pytest.mark.unit
    def test_rate_limit_error_default_retry_after(self) -> None:
        """Test retry_after defaults to 60 seconds."""
        # Act
        error = WorldAnvilRateLimitError("Rate limited")

        # Assert
        assert error.retry_after == 60

    @pytest.mark.unit
    def test_rate_limit_error_with_various_retry_times(self) -> None:
        """Test RateLimitError with various retry_after values."""
        # Arrange
        retry_values = [1, 10, 30, 60, 120, 300, 3600]

        # Act & Assert
        for retry in retry_values:
            error = WorldAnvilRateLimitError("Limited", retry_after=retry)
            assert error.retry_after == retry

    @pytest.mark.unit
    def test_rate_limit_error_inheritance(self) -> None:
        """Test RateLimitError proper inheritance chain."""
        # Act
        error = WorldAnvilRateLimitError("Limited", retry_after=60)

        # Assert
        assert isinstance(error, WorldAnvilRateLimitError)
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_rate_limit_error_catch_as_base(self) -> None:
        """Test RateLimitError can be caught as WorldAnvilError."""
        # Arrange
        error = WorldAnvilRateLimitError("Rate limited", retry_after=60)

        # Act & Assert
        try:
            raise error
        except WorldAnvilError:
            pass  # Expected
        except Exception:
            pytest.fail("Should catch as WorldAnvilError")

    @pytest.mark.unit
    def test_rate_limit_error_catch_specific(self) -> None:
        """Test RateLimitError can be caught specifically."""
        # Arrange
        error = WorldAnvilRateLimitError("Limited", retry_after=120)

        # Act & Assert
        try:
            raise error
        except WorldAnvilRateLimitError as e:
            assert e.retry_after == 120
        except Exception:
            pytest.fail("Should catch as WorldAnvilRateLimitError")

    @pytest.mark.unit
    def test_rate_limit_error_with_zero_retry(self) -> None:
        """Test RateLimitError accepts 0 retry_after."""
        # Act
        error = WorldAnvilRateLimitError("Limited", retry_after=0)

        # Assert
        assert error.retry_after == 0

    @pytest.mark.unit
    def test_rate_limit_error_with_negative_retry(self) -> None:
        """Test RateLimitError accepts negative retry_after."""
        # Act
        error = WorldAnvilRateLimitError("Limited", retry_after=-1)

        # Assert
        assert error.retry_after == -1


class TestWorldAnvilNotFoundError:
    """Tests for resource not found error."""

    @pytest.mark.unit
    def test_not_found_error_instantiation(self) -> None:
        """Test creating WorldAnvilNotFoundError."""
        # Act
        error = WorldAnvilNotFoundError("Article not found")

        # Assert
        assert str(error) == "Article not found"
        assert isinstance(error, WorldAnvilError)

    @pytest.mark.unit
    def test_not_found_error_inheritance(self) -> None:
        """Test NotFoundError proper inheritance chain."""
        # Act
        error = WorldAnvilNotFoundError("Resource not found")

        # Assert
        assert isinstance(error, WorldAnvilNotFoundError)
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_not_found_error_various_messages(self) -> None:
        """Test NotFoundError with various messages."""
        # Arrange
        messages = [
            "Article not found",
            "World not found",
            "Category not found",
            "User not found",
        ]

        # Act & Assert
        for msg in messages:
            error = WorldAnvilNotFoundError(msg)
            assert str(error) == msg

    @pytest.mark.unit
    def test_not_found_error_catch_as_base(self) -> None:
        """Test NotFoundError can be caught as WorldAnvilError."""
        # Arrange
        error = WorldAnvilNotFoundError("Not found")

        # Act & Assert
        try:
            raise error
        except WorldAnvilError:
            pass  # Expected
        except Exception:
            pytest.fail("Should catch as WorldAnvilError")


class TestWorldAnvilValidationError:
    """Tests for validation error."""

    @pytest.mark.unit
    def test_validation_error_instantiation(self) -> None:
        """Test creating WorldAnvilValidationError."""
        # Act
        error = WorldAnvilValidationError("Invalid granularity")

        # Assert
        assert str(error) == "Invalid granularity"
        assert isinstance(error, WorldAnvilError)

    @pytest.mark.unit
    def test_validation_error_inheritance(self) -> None:
        """Test ValidationError proper inheritance chain."""
        # Act
        error = WorldAnvilValidationError("Validation failed")

        # Assert
        assert isinstance(error, WorldAnvilValidationError)
        assert isinstance(error, WorldAnvilError)
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_validation_error_various_messages(self) -> None:
        """Test ValidationError with various messages."""
        # Arrange
        messages = [
            "Invalid granularity (must be string)",
            "Missing required parameter",
            "Payload structure invalid",
            "Invalid parameter type",
        ]

        # Act & Assert
        for msg in messages:
            error = WorldAnvilValidationError(msg)
            assert str(error) == msg

    @pytest.mark.unit
    def test_validation_error_catch_as_base(self) -> None:
        """Test ValidationError can be caught as WorldAnvilError."""
        # Arrange
        error = WorldAnvilValidationError("Validation failed")

        # Act & Assert
        try:
            raise error
        except WorldAnvilError:
            pass  # Expected
        except Exception:
            pytest.fail("Should catch as WorldAnvilError")


class TestExceptionCatchingPatterns:
    """Tests for exception catching patterns across hierarchy."""

    @pytest.mark.unit
    def test_catch_auth_error_specific(self) -> None:
        """Test catching AuthError specifically."""

        # Arrange
        def raise_auth_error() -> None:
            raise WorldAnvilAuthError("Auth failed")

        # Act & Assert
        with pytest.raises(WorldAnvilAuthError):
            raise_auth_error()

    @pytest.mark.unit
    def test_catch_auth_error_as_base(self) -> None:
        """Test catching AuthError as base WorldAnvilError."""

        # Arrange
        def raise_auth_error() -> None:
            raise WorldAnvilAuthError("Auth failed")

        # Act & Assert
        with pytest.raises(WorldAnvilError):
            raise_auth_error()

    @pytest.mark.unit
    def test_catch_api_error_with_status_code(self) -> None:
        """Test catching APIError and accessing status_code."""

        # Arrange
        def raise_api_error() -> None:
            raise WorldAnvilAPIError("Server error", status_code=500)

        # Act & Assert
        try:
            raise_api_error()
        except WorldAnvilAPIError as e:
            assert e.status_code == 500

    @pytest.mark.unit
    def test_catch_rate_limit_with_retry_after(self) -> None:
        """Test catching RateLimitError and accessing retry_after."""

        # Arrange
        def raise_rate_limit() -> None:
            raise WorldAnvilRateLimitError("Limited", retry_after=120)

        # Act & Assert
        try:
            raise_rate_limit()
        except WorldAnvilRateLimitError as e:
            assert e.retry_after == 120

    @pytest.mark.unit
    def test_multiple_exception_handlers(self) -> None:
        """Test multiple exception handlers in correct priority."""

        # Arrange
        def raise_auth_error() -> None:
            raise WorldAnvilAuthError("Auth failed")

        # Act & Assert
        try:
            raise_auth_error()
        except WorldAnvilAuthError:
            pass  # Caught as specific type
        except WorldAnvilError:
            pytest.fail("Should catch as AuthError, not base")

    @pytest.mark.unit
    def test_exception_message_preserved(self) -> None:
        """Test exception message is preserved through raise/catch."""
        # Arrange
        msg = "Specific error message"
        error = WorldAnvilAPIError(msg, status_code=400)

        # Act & Assert
        try:
            raise error
        except WorldAnvilError as e:
            assert str(e) == msg
            assert "Specific error message" in str(e)


class TestExceptionEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_exception_with_empty_message(self) -> None:
        """Test exceptions with empty message."""
        # Arrange & Act
        errors = [
            WorldAnvilError(""),
            WorldAnvilAuthError(""),
            WorldAnvilAPIError(""),
            WorldAnvilRateLimitError(""),
            WorldAnvilNotFoundError(""),
            WorldAnvilValidationError(""),
        ]

        # Assert
        for error in errors:
            assert str(error) == ""

    @pytest.mark.unit
    def test_exception_with_special_chars(self) -> None:
        """Test exceptions with special characters in message."""
        # Arrange
        messages = [
            "Error: 'quoted'",
            'Error with "double quotes"',
            "Error\nwith\nnewlines",
            "Error\twith\ttabs",
            "Error with émojis 🚀",
        ]

        # Act & Assert
        for msg in messages:
            error = WorldAnvilError(msg)
            assert str(error) == msg

    @pytest.mark.unit
    def test_exception_with_very_long_message(self) -> None:
        """Test exceptions with very long messages."""
        # Arrange
        long_msg = "x" * 10000

        # Act
        error = WorldAnvilError(long_msg)

        # Assert
        assert str(error) == long_msg
        assert len(str(error)) == 10000

    @pytest.mark.unit
    def test_api_error_with_large_status_code(self) -> None:
        """Test APIError with large status code."""
        # Act
        error = WorldAnvilAPIError("Error", status_code=999)

        # Assert
        assert error.status_code == 999

    @pytest.mark.unit
    def test_rate_limit_error_with_large_retry(self) -> None:
        """Test RateLimitError with large retry_after value."""
        # Act
        error = WorldAnvilRateLimitError("Limited", retry_after=86400)

        # Assert
        assert error.retry_after == 86400

    @pytest.mark.unit
    def test_exception_repr_string(self) -> None:
        """Test exception repr is valid."""
        # Arrange
        error = WorldAnvilAPIError("Test error", status_code=500)

        # Act
        repr_str = repr(error)

        # Assert
        assert "WorldAnvilAPIError" in repr_str or "Test error" in repr_str
