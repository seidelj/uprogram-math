from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtokens.models import Token
from django.contrib.auth.models import User

class Command(BaseCommand):

    def add_argument(self, parser):
        parser.add_argument('username', nargs="+", type=str)

    def handle(self, *args, **options):
        for username in options['username']:
            try:
                usr = User.objects.get(username=username)
            except:
                self.stdout.write("Invalide username")
            else:
                token, created = Token.objects.get_or_create(user=usr)
                self.stdout.write("Token: {}".format(token.key))


