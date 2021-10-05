from django.core.management.base import BaseCommand, CommandError
from app.people_parser import populate_from_csv

class Command(BaseCommand):
    help = 'Extracts data from form responses to fill the people table. Not perfect but kind does the trick.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help="An exported list of recent form responses in csv.")

    def handle(self, *args, **options):
        populate_from_csv(options["csv_path"])
        