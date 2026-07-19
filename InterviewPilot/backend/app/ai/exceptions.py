class AIError(Exception):
    """Base exception for all AI-related errors."""
    pass


class AIProviderError(AIError):
    """Raised when an AI provider returns an invalid response."""
    pass


class AIValidationError(AIError):
    """Raised when the AI response fails schema validation."""
    pass


class AIRateLimitError(AIError):
    """Raised when the AI provider rate limit is exceeded."""
    pass


class AIAuthenticationError(AIError):
    """Raised when AI provider authentication fails."""
    pass


class AIModelError(AIError):
    """Raised when the requested AI model is unavailable."""
    pass