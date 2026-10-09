import jwt
from django.conf import settings
from datetime import datetime, timedelta


def generate_access_token(payload):
    payload = payload.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.utcnow() + timedelta(minutes=560)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

def generate_refresh_token(payload):
    payload = payload.copy()
    payload["type"] = "refresh"
    payload["exp"] = datetime.utcnow() + timedelta(days=14)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_jwt(token):
   return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])



def extract_email(token):
   toeknDecoded =  decode_jwt(token)
   if toeknDecoded.get("type") != "refresh":
      return "This is not a Refreshtoken"
   
   return toeknDecoded.get("email")

# --- Redis Caching Utils ---
from django.core.cache import cache

def blacklist_token(token):
    """Adds a token to the Redis blacklist with a 14-day expiry to prevent reuse after logout"""
    # Cache key format: blacklist_<token>
    cache.set(f"blacklist_{token}", True, timeout=60 * 60 * 24 * 14)

def is_token_blacklisted(token):
    """Checks if a token exists in the Redis blacklist"""
    return cache.get(f"blacklist_{token}") is not None
