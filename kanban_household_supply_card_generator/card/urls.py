from django.urls import path
from kanban_household_supply_card_generator.card.views import (
    single_card,
    all_cards,
    all_shelf_labels,
)

app_name = "card"
urlpatterns = [
    path("card/", all_cards),
    path("card/<int:pk>/", single_card),
    path("shelf/", all_shelf_labels),
]
