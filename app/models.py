from django.utils import timezone
from django.db import models
from django_extensions.db.fields import RandomCharField


# represents one invoice sent to a member
class ToMemberInvoice(models.Model):
    id = RandomCharField(length=12, primary_key=True)
    
    payed = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    
    created = models.DateField(default=timezone.now)
    
    def __str__(self):
        first_item = self.items.first()
        person_name = "NO PERSON FOUND"
        if first_item is not None:
            person_name = first_item.person.name
        return f"id: {self.id}. Payed: {self.payed}. Person: {person_name}"
        
    def __repr__(self):
        return str(self)
        
    class Meta:
        ordering = ["payed"]
    
# represents someone that orders stuff via us at ETA
class Person(models.Model):
    id = RandomCharField(length=12, primary_key=True)
    
    name = models.TextField(help_text="The name of the person", unique=True)
    email = models.TextField(help_text="How to reach the person the kind way", null=True)
    phone = models.TextField(help_text="How to reach the person the annoying way", null=True)
    
    is_eta = models.BooleanField(help_text="If eta should pay for the stuff", null=True)
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Person, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"Name: {self.name} email: {self.email} Phone: {self.phone} is_eta: {self.is_eta}"
        
    def __repr__(self):
        return str(self)
        
    class Meta:
        ordering = ["name"]
    
# represents one line in the invoice sent by farnell to us
class FarnellItem(models.Model):
    id = RandomCharField(length=12, primary_key=True)
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text="The person to pay")
    cost = models.FloatField(help_text="The amount to pay including VAT")
    item_no = models.TextField(help_text="Item number farnell or TME")
    item_desc = models.TextField(help_text="Description of the item, to make it easy for the payer to know what is payed for")
    created = models.DateField(default=timezone.now, help_text="When this item was added to the database")
    item_count = models.IntegerField(help_text="How many of the item was purchased")
    to_member_invoice = models.ForeignKey(ToMemberInvoice, related_name="items", on_delete=models.CASCADE, help_text="The invoice sent to the member")
    
    order_placed_at = models.DateTimeField(help_text="When the order was placed at farnell or TME")
    invoice_number = models.TextField(help_text="The invoce number as paid by ETA. Used for manual digging")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["item_no", "invoice_number"], name='Item can only appear in same invoice once')
        ]
        
    def __str__(self):
        return f"Name: {self.person.name} Item no: {self.item_no} Count: {self.item_count} Cost: {self.cost}"
        
    def __repr__(self):
        return str(self)
        
    class Meta:
        ordering = ["order_placed_at"]