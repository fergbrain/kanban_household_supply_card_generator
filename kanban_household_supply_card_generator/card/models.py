from django.db import models


class Item(models.Model):

    SUPPLY_TYPE_CHOICES = (("INTERNAL", "Internal"), ("EXTERNAL", "External"))

    name = models.CharField(max_length=255)
    supplier = models.ForeignKey("Supplier", on_delete=models.PROTECT)

    image = models.ImageField(upload_to="images/", null=True)

    additional_information = models.TextField(null=True, blank=True)

    location = models.ForeignKey("Location", on_delete=models.PROTECT, null=True)

    consumption = models.IntegerField(help_text="Weekly")
    time_to_replenish = models.IntegerField(help_text="Days")
    safety_stock = models.IntegerField(help_text="Count")
    reorder_at = models.IntegerField(null=True)

    reorder_qty = models.IntegerField()
    reorder_units = models.CharField(default="ct", max_length=10)

    alt_source_ok = models.BooleanField(
        default=False, help_text="OK to use different manufacturer?"
    )
    alt_supplier_ok = models.BooleanField(
        default=False, help_text="OK to buy from different store?"
    )
    supply_type = models.CharField(
        choices=SUPPLY_TYPE_CHOICES, default="EXTERNAL", max_length=8
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return "%s from %s" % (self.name, self.supplier)


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Location(models.Model):
    region = models.CharField(max_length=30)
    rack = models.CharField(max_length=30)
    shelf = models.CharField(max_length=30)

    class Meta:
        ordering = (
            "region",
            "rack",
            "shelf",
        )

    def __str__(self):
        return "%s: Rack %s, Shelf %s" % (self.region, self.rack, self.shelf)
