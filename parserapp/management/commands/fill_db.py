from django.core.management.base import BaseCommand
from parserapp.models import Vacancy, Skills_table, Params
from parserapp.parser  import hh_serch

# from usersapp.blogapp.models import Poll
class Command(BaseCommand):
        def handle(self, *args, **options):
                # print('fdghjkl')
                hh_serch('python', 'name')