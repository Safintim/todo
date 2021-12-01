from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate local db'

    def handle(self, *args, **options):
        call_command("migrate")
        User.objects.create_superuser(username='root', password='root')
        self.stdout.write(self.style.SUCCESS('Successfully create superuser'))
