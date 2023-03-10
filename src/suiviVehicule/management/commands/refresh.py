from django.core.management.base import BaseCommand, CommandError
from suiviVehicule.services import services
class Command(BaseCommand):

    def handle(self, *args, **options):
        services().rechange()
        services().gestion_status_pos()
        print("themmmmmeeeeeeeeeeeeeeeeeeee")
        return 