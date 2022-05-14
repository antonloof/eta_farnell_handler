from django.core.management.base import BaseCommand, CommandError
from app.models import FarnellItem
from django.db.models import Sum, Q

class Command(BaseCommand):
    help = 'Calculates the biggest farnell spenders!'

    def add_arguments(self, parser):
        parser.add_argument('since_date', help="Since when to get data from")

    def handle(self, *args, **options):
        all = (FarnellItem.objects.all()
            .filter(created__gt=options["since_date"])
            .filter(~Q(person__is_eta=True))
            .values("person__name")
            .annotate(total_spending=Sum("cost"))
            .order_by()
        )
        print("Name,Spent")
        for item in all:
            print(item["person__name"],",",round(item["total_spending"]), sep="")
        
        