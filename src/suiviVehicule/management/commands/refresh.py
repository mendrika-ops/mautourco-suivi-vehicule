from django.core.management.base import BaseCommand, CommandError
from suiviVehicule.services import services
import subprocess
class Command(BaseCommand):

    def handle(self, *args, **options):
        services().refresh()
        print("--------------terminer-------------")
        return 