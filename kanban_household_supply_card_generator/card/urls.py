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
    path("card/<str:region>/<str:rack>/<str:shelf>/", all_cards),
    path("card/<str:region>/<str:rack>/", all_cards),
    path("card/<str:region>/", all_cards),
    path("shelf/<str:region>/<str:rack>/<str:shelf>/", all_shelf_labels),
    path("shelf/<str:region>/<str:rack>/", all_shelf_labels),
    path("shelf/<str:region>/", all_shelf_labels),
    path("shelf/", all_shelf_labels),
]
