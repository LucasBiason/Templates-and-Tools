
import pytz
from datetime import datetime

from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from authentication.exceptions import raise_invalid_token, raise_user_not_active, \
    raise_expired_token


class ExpiringTokenAuthentication(TokenAuthentication):
    
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return raise_invalid_token()

        if not token.user.is_active:
            return raise_user_not_active()

        utc_now = datetime.utcnow()
        tzinfo=pytz.timezone(settings.TIME_ZONE)
        utc_now = utc_now.replace(tzinfo=tzinfo)
        token_created = token.created.replace(tzinfo=tzinfo)
        
        if token_created < utc_now - settings.TOKEN_EXPIRE_TIME:
            return raise_expired_token()

        return token.user, token
