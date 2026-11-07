import secrets
import hashlib
from api.models import APIKey



def generate_api_key(organization, name):
    raw_key = secrets.token_urlsafe(32)

    prefix = raw_key[:12]

    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()

    api_key = APIKey.objects.create(
        organization=organization,
        name=name,
        prefix=prefix,
        hashed_key=hashed_key,
    )

    return api_key, raw_key
