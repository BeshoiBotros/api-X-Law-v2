import jwt
from channels.middleware import BaseMiddleware
from .settings import SECRET_KEY

def get_user(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Expired Token")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid Token: {e}")
        return None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None
    
class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get('headers', []))

        authorization_header = headers.get(b'authorization', b'').decode('utf-8')
        if authorization_header.startswith('Bearer '):
            token = authorization_header[len('Bearer '):].strip()
            user = get_user(token)

            if user:
                scope['user'] = user

        return await super().__call__(scope, receive, send)
