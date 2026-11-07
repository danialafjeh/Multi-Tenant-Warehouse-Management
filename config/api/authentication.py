import hashlib
import hmac
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from api.models import APIKey



class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if auth[0].lower() != b"api-key":
            return None

        if len(auth) != 2:
            raise AuthenticationFailed("Invalid API Key header.")

        raw_key = auth[1].decode("utf-8")

        prefix = raw_key[:12]

        api_key = ( 
            APIKey.objects.select_related("organization")
            .filter(prefix=prefix, is_active=True,)
            .first()
        )

        if not api_key:
            raise AuthenticationFailed("Invalid API Key.")

        hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()

        if not hmac.compare_digest(hashed_key, api_key.hashed_key):
            raise AuthenticationFailed("Invalid API Key.")

        APIKey.objects.filter(pk=api_key.pk).update(last_used_at=timezone.now())

        return api_key.organization, api_key

    def authenticate_header(self, request):
        return "Api-Key"
