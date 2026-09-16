from fastapi import Header, HTTPException, status

# In production, load this from an environment variable — never hardcode it.
API_KEY = "supersecret-api-key-123"


def verify_api_key(x_api_key: str = Header(...)):
    """Every protected endpoint requires header:  X-API-Key: supersecret-api-key-123"""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key
