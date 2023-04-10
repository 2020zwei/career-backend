import os
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email='admin1@gmail.com').exists():
            User.objects.create_superuser('admin1@gmail.com',
                                          'admin@123')