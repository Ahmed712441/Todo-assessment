from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.encoding import force_str
from rest_framework.authentication import (
    get_authorization_header,
)

from rest_framework_jwt.blacklist.exceptions import (
    InvalidAuthorizationCredentials,
)
from rest_framework_jwt.compat import gettext_lazy as _
from rest_framework_jwt.settings import api_settings

class Auth0BackendAuthentication(JSONWebTokenAuthentication):

    def get_token_from_request(self, request):
        try:
            authorization_header = force_str(get_authorization_header(request))

            self.token = self.get_token_from_authorization_header(authorization_header)
        except (InvalidAuthorizationCredentials, UnicodeDecodeError):
            self.token = self.get_token_from_cookies(request.COOKIES)

        return self.token
    
    def jwt_get_username_from_payload(self, *args, **kwargs):
        return api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(*args, **kwargs,token=self.token)