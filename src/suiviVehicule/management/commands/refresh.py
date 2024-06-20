import sys
from django.core.management.base import BaseCommand, CommandError
from suiviVehicule.services import services
import subprocess
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            print("--------------------------- beginning --------------------------")
            services().refresh()
            print("--------------------------- finishing --------------------------")
            sys.exit()
        except Exception as e:
            sys.exit()
        finally:
            sys.exit()
        return 