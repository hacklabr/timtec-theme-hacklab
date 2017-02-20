# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction

import unicodecsv


User = get_user_model()

sizes = {
    'username': 30,
    'last_name': 30,
    'first_name': 30,
}


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 1:
            raise CommandError('Choose a file to import')

        # This file comes from moodle's DB and generates only deactivated users
        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]

                user, created = User.objects.get_or_create(email=row['email'])
                if created and not User.objects.filter(username=row['username'][:29]):
                    user.username = row['username'][:29]
                elif created:
                    user.username = row['email'][:28].split('@')[0] + "2"

                user.first_name = row['firstname'][:29]
                user.last_name = row['lastname'][:29]
                user.city = row['city'][:29]
                user.biography = row['description']

                user.is_active = False
                user.accepted_terms = False
                user.save()
