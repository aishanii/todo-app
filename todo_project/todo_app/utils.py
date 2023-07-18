import datetime
from .models import MainUser
from django.db.models.functions import Substr
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .constants import JWT_EXP_TIME

def generate_access_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXP_TIME)
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

def validate_email_password(email, password):
    from .constants import EMAIL_NOT_REGISTERED
    try:
        user = MainUser.objects.get(email=email)
        if user.check_password(password):
            return True
        else:
            return False
    except MainUser.DoesNotExist:
        raise Exception(EMAIL_NOT_REGISTERED)
    except:
        return False