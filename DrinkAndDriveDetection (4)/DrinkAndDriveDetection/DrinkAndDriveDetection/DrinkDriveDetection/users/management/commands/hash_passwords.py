# yourapp/management/commands/hash_passwords.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Hash plain text passwords for existing users'

    def handle(self, *args, **kwargs):
        UserModel = get_user_model()
        users = UserModel.objects.all()

        for user in users:
            if not user.password.startswith('pbkdf2_sha256$'):
                user.set_password(user.password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Updated password for user: {user.email}'))

        self.stdout.write(self.style.SUCCESS('Successfully hashed all plain text passwords.'))
