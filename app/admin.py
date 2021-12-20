from django.contrib import admin
from app.models import ToMemberInvoice, Person, FarnellItem

class FarnellItemAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "to_member_invoice":
            kwargs["queryset"] = ToMemberInvoice.objects.filter(sent=False, payed=False)
        return super(FarnellItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    
class ToMemberInvoiceAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    
admin.site.register(ToMemberInvoice, ToMemberInvoiceAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(FarnellItem, FarnellItemAdmin)