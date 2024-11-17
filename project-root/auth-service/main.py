# auth-service/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional

app = FastAPI()
security = HTTPBearer()

# Environment variables with defaults for development
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

class Credentials(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"

class ValidationResponse(BaseModel):
    valid: bool
    username: Optional[str] = None

def create_token(username: str) -> str:
    """Create a new JWT token."""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    token_data = {
        "sub": username,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)

def validate_token(token: str) -> dict:
    """Validate the JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: Credentials):
    """Login endpoint that validates credentials and returns a JWT token."""
    # In a real application, validate against a database
    # This is a simplified example
    if credentials.username == "user" and credentials.password == "pass":
        token = create_token(credentials.username)
        return TokenResponse(token=token)
    
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

@app.post("/auth/validate", response_model=ValidationResponse)
async def validate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate the JWT token and return the associated username."""
    try:
        payload = validate_token(credentials.credentials)
        return ValidationResponse(
            valid=True,
            username=payload.get("sub")
        )
    except HTTPException as e:
        return ValidationResponse(valid=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

