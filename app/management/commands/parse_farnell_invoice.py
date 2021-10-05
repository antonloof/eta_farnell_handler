from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from app.parse_farnell_invoice import parse_and_save_multiple_invoices

class Command(BaseCommand):
    help = 'Parses a farnell invoice'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs="+", help="The file(s) to parse")

    def handle(self, *args, **options):
        parse_and_save_multiple_invoices(options["file"])
        