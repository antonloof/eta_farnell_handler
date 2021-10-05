from pathlib import Path
from app.models import Person
import csv
from collections import defaultdict

def populate_from_csv(path):
    mail_by_name = defaultdict(str)
    phone_by_name = defaultdict(str)
    
    with Path(path).open(encoding ="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            if len(row) < 9:
                continue
            if not row[3]:
                continue
            order_line = row[3].split("\n")[0]
            if not order_line:
                continue
            order_line_split = order_line.split(",")
            if len(order_line_split) != 3:
                continue
            name = order_line_split[2].strip().upper()
            
            if row[1]:
                email = row[1]
                if not mail_by_name[name]:
                    mail_by_name[name] = email
            if row[8]:
                phone = row[8]
                if not phone_by_name[name]:
                    phone_by_name[name] = phone
            
    for name, email in mail_by_name.items():
        person, _ = Person.objects.get_or_create(name=name)
        if person.email:
            continue
        person.email = email
        person.save()
        print("Person", name, "now has email:", email)
        
    for name, phone in phone_by_name.items():
        person, _ = Person.objects.get_or_create(name=name)
        if person.phone:
            continue
        person.phone = phone
        person.save()
        print("Person", name, "now has phone:", phone)
            
    
def get_boolean_input(prompt):
    while True:
        inp = input(prompt + " [y/n]: ")
        if inp == "y":
            return True
        elif inp == "n":
            return False
    
def ask_if_is_eta():
    for person in Person.objects.all().filter(is_eta__is_null=True):
        person.is_eta = get_boolean_input("Is person {person.name} bying for ETA?")
        person.save()
        print("Person", person.name, "should not pay invoices" if person.is_eta else "should pay invoices")