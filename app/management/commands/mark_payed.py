from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import ToMemberInvoice

class Command(BaseCommand):
    help = 'Marks an invoice as payed. Good for writing down when the members pay up!'

    def add_arguments(self, parser):
        parser.add_argument('id', help="The id of the invoice that is payed")

    def handle(self, *args, **options):
        try:
            invoice = ToMemberInvoice.objects.get(id=options["id"])
        except ToMemberInvoice.DoesNotExist:
            print("Could not find invoice", options["id"])
            return
            
        invoice.payed = True
        invoice.save()
        
        total_amount = sum([item.cost for item in invoice.items.all()])
        print("Invoice:", invoice, "for person", invoice.items.first().person.name, "is payed. Total cost:", total_amount)