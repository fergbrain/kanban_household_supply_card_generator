from django.contrib import admin
from .models import Item, Supplier, Location
from .forms import ItemForm
from django.db.models import Count


class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ["name", "updated_date"]
    list_filter = ["location", "location__region", "location__rack", "updated_date"]
    search_fields = ["name"]


class LocationAdmin(admin.ModelAdmin):

    # https://stackoverflow.com/a/62952381/3642184
    def location_count(self, obj):
        return obj.location_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(location_count=Count("item", distinct=True))
        return queryset

    location_count.admin_order_field = 'location_count'
    list_display = ["__str__", "location_count"]
    list_filter = ["region", "rack"]


admin.site.register(Item, ItemAdmin)
admin.site.register(Supplier)
admin.site.register(Location, LocationAdmin)
