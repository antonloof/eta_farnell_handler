from django.contrib import admin
from app.models import ToMemberInvoice, Person, FarnellItem

class FarnellItemAdmin(admin.ModelAdmin):
    pass
    
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    
class ToMemberInvoiceAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    
admin.site.register(ToMemberInvoice, ToMemberInvoiceAdmin)
    
admin.site.register(Person, PersonAdmin)
admin.site.register(FarnellItem, FarnellItemAdmin)