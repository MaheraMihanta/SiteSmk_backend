from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserRole


class Command(BaseCommand):
    help = 'Creer un compte administrateur avec privileges complets.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--email', default='')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Utilisateur deja existant.'))
            return

        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = UserRole.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Administrateur cree avec succes.'))
