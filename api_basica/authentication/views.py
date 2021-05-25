import pytz
from datetime import datetime

from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CreateTokenView(APIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def raise_access_denied(self, msg):
        raise Exception(msg, status_code=401)
    
    def get_object(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
            }
        )
        
        valid = serializer.is_valid()
        if not valid:
            self.raise_access_denied("Unable to login with provided credentials")
                
        user = serializer.validated_data['user']
        return user

    def create_token(self, user):
        """
        Create new token and return expire time.
        """
        Token.objects.filter(user=user).delete()  # clear token user
        token = Token.objects.create(user=user)  # create new token
        return token

    def check_expire(self, user):
        """
        Check token user not expired.
        """
        token = Token.objects.filter(user=user).first()

        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token:
            time_expired = utc_now - settings.TOKEN_EXPIRE_TIME
            expired = token.created < time_expired
        else:
            expired = True

        return token, expired
        
    def post(self, request, *args, **kwargs):
        user = self.get_object(request)
        
        token, expired = self.check_expire(user)
        if expired:
            token = self.create_token(user)
        expire = token.created + settings.TOKEN_EXPIRE_TIME

        return Response({
            'token': token.key, 
            'expire': expire
        })

