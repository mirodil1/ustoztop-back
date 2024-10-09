import jwt
from core.config import JWT_ALGORITHM, JWT_PUBLIC_KEY
from jwt import PyJWTError
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)


class User(BaseUser):
    """Класс пользователя."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        """Authenticated status."""
        return True

    @property
    def display_name(self) -> str:
        """User display name"""
        return f"user_id={self.user_id}"


class JWTAuthBackend(AuthenticationBackend):
    """Class for working with authorization."""

    async def authenticate(self, request):
        """User authorization."""
        # Get JWT token from user's cookies

        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return
        except ValueError as err:
            raise AuthenticationError("Invalid authorization") from err

        # Returns UnauthenticatedUser if token does not exists in header
        if not token:
            return
        # Checks the validity of the JWT token,
        # if token is invalid returns UnauthenticatedUser object
        try:
            jwt_decoded = jwt.decode(
                token,
                JWT_PUBLIC_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except PyJWTError as err:
            raise AuthenticationError("Invalid credentials")
        # In case if token is valid returns an object of the authorized user
        permissions = "write"

        return AuthCredentials(permissions), User(user_id=jwt_decoded["sub"])
