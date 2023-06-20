from django.core.management.base import BaseCommand, CommandError
from suiviVehicule.services import services
class Command(BaseCommand):

    def handle(self, *args, **options):
        services().refresh()
        print("themmmmmeeeeeeeeeeeeeeeeeeee")
        return 