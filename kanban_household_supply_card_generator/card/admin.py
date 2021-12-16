from django.contrib import admin
from .models import Item, Supplier, Location
from .forms import ItemForm


class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_filter = ["location__region", "location__rack", "updated_date"]


admin.site.register(Item, ItemAdmin)
admin.site.register(Supplier)
admin.site.register(Location)
