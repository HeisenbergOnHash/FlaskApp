import jwt,uuid,os,datetime
from flask import request

SECRET_KEY = "namithaGuntupalli"

def create_access_token(username, role):
    current_time = datetime.datetime.utcnow()
    payload = {
        "sub": username,"role": role,"iat": int(current_time.timestamp()),        # Use UTC timestamp for issued at
        "exp": int((current_time + datetime.timedelta(minutes=5)).timestamp())    # Use UTC timestamp for expiration
              }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_access_token():
    try:
        payload = jwt.decode(request.cookies.get('token_cookie'), SECRET_KEY, algorithms=["HS256"])
        return {"status": "valid", "message": "Token is valid", "data": payload, "valid": True}
    except jwt.ExpiredSignatureError:
        return {"status": "expired", "message": "Token has expired", "valid": False}
    except jwt.InvalidSignatureError:
        return {"status": "invalid_signature", "message": "Invalid token signature", "valid": False}
    except jwt.InvalidAlgorithmError:
        return {"status": "invalid_algorithm", "message": "Algorithm not allowed", "valid": False} 
    except jwt.MissingRequiredClaimError as e:
        return {"status": "missing_claim", "message": f"Missing claim: {str(e)}", "valid": False} 
    except jwt.ImmatureSignatureError:
        return {"status": "immature_signature", "message": "Token is not yet valid", "valid": False}
    except jwt.InvalidAudienceError:
        return {"status": "invalid_audience", "message": "Invalid audience claim", "valid": False}
    except jwt.InvalidIssuerError:
        return {"status": "invalid_issuer", "message": "Invalid issuer claim", "valid": False}
    except jwt.InvalidIssuedAtError:
        return {"status": "invalid_iat", "message": "Invalid issued at (iat) claim", "valid": False}
    except jwt.InvalidTokenError:  
        return {"status": "invalid", "message": "Invalid token", "valid": False}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}", "valid": False}

def extend_cookie_expiration(response):
  token = request.cookies.get('token_cookie')
  if token:
    expires = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=10)).timestamp()) 
    response.set_cookie('token_cookie', token, expires=expires,httponly=True, secure=True, samesite=None)
  return response
