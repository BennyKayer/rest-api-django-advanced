import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django Command to pause execution until database is available

    Args:
        BaseCommand (class):
        https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/#django.core.management.BaseCommand
    """

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
