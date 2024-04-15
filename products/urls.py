from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("products/", views.products, name='product'),
    path("about/", views.about, name='about'),
    path("details/<int:product_id>/", views.details, name='detail'),  # This line sets up a URL pattern for displaying detailed information about a product identified by its integer ID which is the primary key.
    path("search/", views.search, name='search'),

]