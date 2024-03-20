from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from jose import JWTError, jwt
import secrets

# Constants for JWT token creation and verification
SECRET_KEY = "a very secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5  # token expiry limit in minutes

# Initialize HTTPBasic auth scheme
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(credentials: HTTPBasicCredentials) -> HTTPBasicCredentials:
    """
    Authenticate user by comparing the provided credentials with the expected ones.

    Parameters:
        credentials (HTTPBasicCredentials): The credentials to authenticate.

    Returns:
        HTTPBasicCredentials: The authenticated user's credentials.

    Raises:
        HTTPException: If authentication fails.
    """
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with a specified expiration time.

    Parameters:
        data (dict): The payload data to include in the token.
        expires_delta (Optional[timedelta]): The expiration time from now. Default is None, uses global setting.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Here you can add more checks, for example, against a database to see if the user exists
    except JWTError:
        raise credentials_exception
    return username


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
