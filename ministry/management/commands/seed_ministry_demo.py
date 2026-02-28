from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserRole
from ministry.models import ChatMessage, Entity, FinanceEntry, LeadershipMember, LeadershipRole, NewsItem, Post
from ministry.services import provision_entity_account

User = get_user_model()


class Command(BaseCommand):
    help = 'Charge des donnees minimales pour le frontend young-faith.'

    def handle(self, *args, **options):
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jeunesse.local',
                'display_name': 'Administrateur',
                'is_staff': True,
                'is_superuser': True,
                'role': UserRole.ADMIN,
            },
        )
        if created:
            admin_user.set_password('Admin123!')
            admin_user.save(update_fields=['password'])

        national, _ = Entity.objects.get_or_create(
            code='bureau-national',
            defaults={
                'name': 'Bureau National Jeunesse',
                'city': 'National',
                'contact': '+237 600 000 000',
                'leader': 'President National',
                'members': 12,
                'is_national_office': True,
                'description': 'Coordination nationale des groupes de jeunesse.',
            },
        )

        offices = [
            ('douala', 'Entite Douala', 'Douala', 'Frere Jean', 45),
            ('yaounde', 'Entite Yaounde', 'Yaounde', 'Soeur Marie', 62),
            ('bafoussam', 'Entite Bafoussam', 'Bafoussam', 'Frere Paul', 30),
        ]

        entities = [national]
        for code, name, city, leader, members in offices:
            entity, _ = Entity.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'city': city,
                    'contact': '+237 6XX XXX XXX',
                    'leader': leader,
                    'members': members,
                    'description': f'{name} - rassemblement local.',
                },
            )
            entities.append(entity)

        leadership_defaults = [
            (LeadershipRole.PRESIDENT, 'President National'),
            (LeadershipRole.VICE_PRESIDENT_1, 'Vice-President 1'),
            (LeadershipRole.VICE_PRESIDENT_2, 'Vice-President 2'),
            (LeadershipRole.TREASURER, 'Tresorier National'),
            (LeadershipRole.FINANCIAL_SECRETARY, 'Secretaire Financier'),
            (LeadershipRole.SECRETARY_GENERAL_1, 'Secretaire General 1'),
            (LeadershipRole.SECRETARY_GENERAL_2, 'Secretaire General 2'),
            (LeadershipRole.COUNSELOR_1, 'Conseiller 1'),
            (LeadershipRole.COUNSELOR_2, 'Conseiller 2'),
            (LeadershipRole.COUNSELOR_3, 'Conseiller 3'),
            (LeadershipRole.COUNSELOR_4, 'Conseiller 4'),
        ]

        for role, name in leadership_defaults:
            LeadershipMember.objects.get_or_create(entity=national, role=role, defaults={'member_name': name})

        default_passwords = {
            'bureau-national': 'National123!',
            'douala': 'Douala123!',
            'yaounde': 'Yaounde123!',
            'bafoussam': 'Bafoussam123!',
        }

        for entity in entities:
            if not hasattr(entity, 'account'):
                email = f"{entity.code}@jeunesse.local"
                display_name = entity.name
                account, generated_password = provision_entity_account(
                    entity=entity,
                    email=email,
                    display_name=display_name,
                    created_by=admin_user,
                )
                self.stdout.write(f"Compte provisionne pour {entity.name} ({email}) - mdp initial: {generated_password}")
            else:
                account = entity.account

            fixed_password = default_passwords.get(entity.code, 'Jeunesse123!')
            account.user.set_password(fixed_password)
            account.user.save(update_fields=['password'])
            self.stdout.write(f"Mot de passe demo fixe pour {entity.name}: {fixed_password}")

        NewsItem.objects.get_or_create(
            title='Grande Conference de la Jeunesse 2026',
            defaults={
                'summary': 'Trois jours de louange, enseignement et communion fraternelle.',
                'published_at': date.today() + timedelta(days=15),
            },
        )
        NewsItem.objects.get_or_create(
            title='Campagne d evangelisation nationale',
            defaults={
                'summary': 'Lancement de la campagne dans 12 villes.',
                'published_at': date.today() + timedelta(days=5),
            },
        )

        finance_entries = [
            ('Dime mensuelle', 350000),
            ('Location salle conference', -120000),
            ('Don special', 500000),
            ('Materiel sonorisation', -250000),
        ]
        for label, amount in finance_entries:
            FinanceEntry.objects.get_or_create(
                label=label,
                amount=amount,
                entity=national,
                recorded_at=date.today(),
            )

        for entity in entities:
            author = entity.account.user
            Post.objects.get_or_create(
                author=author,
                content=f"Shalom depuis {entity.name}. Que Dieu vous benisse.",
                defaults={'likes_count': 10, 'comments_count': 2},
            )

        if not ChatMessage.objects.exists():
            for entity in entities:
                ChatMessage.objects.create(
                    author=entity.account.user,
                    message=f"Shalom a tous, message de {entity.name}.",
                )

        self.stdout.write(self.style.SUCCESS('Donnees de demo chargees.'))
        self.stdout.write('Admin demo: admin@jeunesse.local / Admin123!')

