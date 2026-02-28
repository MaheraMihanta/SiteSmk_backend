import re
import secrets
import string

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import UserRole

from .models import Entity, EntityAccount

User = get_user_model()


def generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + '!@#$%'
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
            return password


def build_username(email: str) -> str:
    base = re.sub(r'[^a-z0-9_]+', '_', email.split('@')[0].lower()).strip('_') or 'entity'
    candidate = base
    idx = 1
    while User.objects.filter(username=candidate).exists():
        idx += 1
        candidate = f"{base}_{idx}"
    return candidate


@transaction.atomic
def provision_entity_account(*, entity: Entity, email: str, display_name: str, created_by=None):
    if hasattr(entity, 'account'):
        raise ValueError('Cette entite possede deja un compte.')

    username = build_username(email)
    password = generate_password()

    role = UserRole.NATIONAL if entity.is_national_office else UserRole.ENTITY
    user = User.objects.create_user(
        username=username,
        email=email.lower(),
        password=password,
        role=role,
        display_name=display_name.strip(),
        is_active=True,
    )

    account = EntityAccount.objects.create(
        user=user,
        entity=entity,
        created_by=created_by,
    )

    return account, password

