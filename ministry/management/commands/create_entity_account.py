from django.core.management.base import BaseCommand, CommandError

from ministry.models import Entity
from ministry.services import provision_entity_account


class Command(BaseCommand):
    help = 'Provisionne un compte pour une entite et genere automatiquement le mot de passe.'

    def add_arguments(self, parser):
        parser.add_argument('--entity-id', type=int, required=True, help='ID de l entite')
        parser.add_argument('--email', type=str, required=True, help='Email de connexion du compte')
        parser.add_argument('--display-name', type=str, required=True, help='Nom public du compte')

    def handle(self, *args, **options):
        entity_id = options['entity_id']
        email = options['email']
        display_name = options['display_name']

        try:
            entity = Entity.objects.get(id=entity_id, is_active=True)
        except Entity.DoesNotExist as exc:
            raise CommandError('Entite introuvable ou inactive.') from exc

        try:
            account, generated_password = provision_entity_account(
                entity=entity,
                email=email,
                display_name=display_name,
                created_by=None,
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.SUCCESS('Compte cree avec succes.'))
        self.stdout.write(f"Entite: {account.entity.name}")
        self.stdout.write(f"Email: {account.user.email}")
        self.stdout.write(f"Mot de passe genere: {generated_password}")

