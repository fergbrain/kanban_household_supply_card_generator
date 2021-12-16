from django import forms
from .models import Item
import calculation


class ItemForm(forms.ModelForm):
    reorder_at = forms.IntegerField(
        widget=calculation.FormulaInput("consumption/7*time_to_replenish+safety_stock")
    )

    class Meta:
        fields = "__all__"
        model = Item
