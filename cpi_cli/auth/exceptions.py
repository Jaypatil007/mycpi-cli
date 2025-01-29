class AuthenticationError(Exception):
    """Base exception for authentication errors"""
    pass

class TokenRefreshError(AuthenticationError):
    """Raised when token refresh fails"""
    pass