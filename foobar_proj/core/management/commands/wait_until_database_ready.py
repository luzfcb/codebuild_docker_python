from pprint import pprint
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        database_offline = True
        max_tries = 10
        count = 0
        while database_offline and count != max_tries:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1')
                    cursor.fetchone()
            except Exception as e:
                pprint("DATABASE:")
                pprint(settings.DATABASES, indent=4, width=200)
                pprint("Exception:")
                print(str(e))
                print("count:", count)
                sleep(1)
                count += 1
            else:
                database_offline = False
