from django.core.management.base import BaseCommand, CommandError
from app.models import Person

class Command(BaseCommand):
    help = 'Updates a person manualy! Just what you need sometimes!'

    def add_arguments(self, parser):
        parser.add_argument('name', help="The name of the person to update")
        parser.add_argument('--phone', help="The phone number to set to")
        parser.add_argument('--email', help="The email address to set to")
        parser.add_argument('--is_eta', help="y to set as ETA, n to set as not ETA")

    def handle(self, *args, **options):
        person, created = Person.objects.get_or_create(name=options["name"].upper())
        if created:
            print("Person was not in database, created one instead. Name: ", person.name)
        if options["phone"] is not None:
            person.phone = options["phone"]
        if options["email"] is not None:
            person.email = options["email"]
        if options["is_eta"] is not None:
            if options["is_eta"].lower() == "y":
                person.is_eta = True
            elif options["is_eta"].lower() == "n":
                person.is_eta = False
        person.save()
        print("Person saved. Current state:", person)
        