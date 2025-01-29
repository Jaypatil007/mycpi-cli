from abc import ABC, abstractmethod
from typing import Optional, Dict
import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AuthProvider(ABC):
    """Abstract base class for authentication providers"""
    
    @abstractmethod
    def get_token(self) -> str:
        """Get valid authentication token"""
        pass

    @abstractmethod
    def is_token_valid(self) -> bool:
        """Check if current token is valid"""
        pass

class OAuthProvider(AuthProvider):
    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        # Add 5-minute buffer before token expiry
        self._expiry_buffer = timedelta(minutes=5)

    def get_token(self) -> str:
        """Get a valid OAuth token, refreshing if necessary"""
        try:
            if not self.is_token_valid():
                self._refresh_token()
            return self._token
        except Exception as e:
            logger.error(f"Failed to get token: {str(e)}")
            raise AuthenticationError(f"Failed to obtain OAuth token: {str(e)}")

    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired"""
        if not self._token or not self._token_expiry:
            return False
        return datetime.now() < (self._token_expiry - self._expiry_buffer)

    def _refresh_token(self) -> None:
        """Fetch a new OAuth token"""
        try:
            response = requests.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            response.raise_for_status()
            token_data = response.json()
            
            self._token = token_data["access_token"]
            # Set token expiry if provided, default to 1 hour if not
            expires_in = int(token_data.get("expires_in", 3600))
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            logger.debug("Successfully refreshed OAuth token")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise AuthenticationError(f"Failed to refresh OAuth token: {str(e)}")