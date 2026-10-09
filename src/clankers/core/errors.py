class ClankersError(Exception):
    """Base Exception for all clankers errors"""

class LLMError(ClankersError):
    """Base Exception for LLM related failures"""
    def __init__(self, message: str, *, provider: str | None = None, status_code: int | None = None, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code
        self.retry_after = retry_after

class LLMTimeoutError(LLMError):
    """The LLM request exceeded its timeout."""

class LLMConnectionError(LLMError):
    """The provider could not be reached."""

class LLMRatelimitError(LLMError):
    """The provider rejected the request due to rate limiting."""

class LLMAuthenticationError(LLMError):
    """The provider rejected the supplied credentials."""

class LLMInvalidRequestError(LLMError):
    """The LLM rejected the request as invalid."""

class LLMProviderError(LLMError):
    """The provider returned an unsuccessful response."""

class LLMResponseError(LLMError):
    """The provider returned a malformed or unexpected response."""