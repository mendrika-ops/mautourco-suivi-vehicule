import sys
from django.core.management.base import BaseCommand, CommandError
from suiviVehicule.services import services
import subprocess
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            subprocess.call('taskkill /IM cmd.exe /F', shell=True)
            services().refresh()
            print("themmmmmeeeeeeeeeeeeeeeeeeee")
            self.exit_code = 1
            self.handle_internal(*args, **kwargs)
            sys.exit(self.exit_code)
        except Exception:
            self.exit_code = 0
            self.handle_internal(*args, **kwargs)
            sys.exit(self.exit_code)
        return 