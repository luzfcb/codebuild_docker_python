import sys
import traceback
import argparse
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.db import connection


def positive_number(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f'Expected a positive integer, obtained "{value}"')
    else:
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"Value must be greater than or equal to 1")
        return ivalue


class Command(BaseCommand):
    default_timeout = 90

    @property
    def help(self, ):
        return f"Repeatedly try to connect and query the database until a timeout. " \
            f"Will exit immediately with a zero status if successful connect and query the database " \
            f"or will exit with a non-zero status if it is impossible " \
            f"(Default timeout: {self.default_timeout}s)"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--timeout",
            dest="timeout",
            type=positive_number,
            default=self.default_timeout,
            help=f"Timeout in seconds to automatically stop execution (Default: {self.default_timeout})",
        )

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        database_unavailable = True
        exit_code = 1
        now_datetime = datetime.now()

        timeout = now_datetime + timedelta(seconds=options["timeout"])

        while database_unavailable and now_datetime <= timeout:
            try:
                with connection.cursor() as cursor:
                    query = 'SELECT 1 + 1 as result'
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if verbosity > 2:
                        self.stdout.write(f"QUERY: {query}\nResult: {result}")
            except Exception as e:  # noqa
                if verbosity > 2:
                    self.stdout.write(traceback.format_exc())
                sleep(1)
                now_datetime = datetime.now()
            else:
                exit_code = 0
                database_unavailable = False
        if exit_code:
            if verbosity > 1:
                self.stdout.write("Impossible to connected to the database")
        else:
            if verbosity > 1:
                self.stdout.write("Successfully connected to the database")

        sys.exit(exit_code)
