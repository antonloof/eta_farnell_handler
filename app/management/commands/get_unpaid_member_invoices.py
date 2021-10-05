from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from app.mail_generator import generate_invoice_mails

class Command(BaseCommand):
    help = 'Gets all emails to send to the people'

    def add_arguments(self, parser):
        parser.add_argument('output_folder', help="Where to dump the HTML mails.")

    def handle(self, *args, **options):
        generate_invoice_mails(options["output_folder"])
        