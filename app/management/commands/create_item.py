from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import Person, FarnellItem, ToMemberInvoice

class Command(BaseCommand):
    help = 'Updates a person manualy! Just what you need sometimes!'

    def add_arguments(self, parser):
        parser.add_argument('name', help="The name of the person give the invoice to")
        parser.add_argument('--cost', help="How much it costs", type=float, required=True)
        parser.add_argument('--item_no', help="An identifying number for the item", default="UNKNOWN")
        parser.add_argument('--item_desc', help="Description of the item", default="Item is not known")
        parser.add_argument('--item_count', help="How many items", type=int, default=1)
        parser.add_argument('--order_placed_at', help="When was the order placed", default=timezone.now())
        parser.add_argument('--invoice_number', help="Something that identifies the invoid", default="UNKNOWN")

    def handle(self, *args, **options):
        person, created = Person.objects.get_or_create(name=options["name"].upper())
        if created:
            print("Person was not in database, created one instead. Name: ", person.name)
        item = FarnellItem(
            person=person, 
            cost=options["cost"], 
            item_no=options["item_no"], 
            item_desc=options["item_desc"], 
            item_count=options["item_count"], 
            order_placed_at=options["order_placed_at"], 
            invoice_number=options["invoice_number"]
        )
        # try to place the item to some invoice 
        invoice, _ = ToMemberInvoice.objects.get_or_create(sent=False, payed=False, items__person=person)
        item.to_member_invoice = invoice
        item.save()
        print("Created item:", item)