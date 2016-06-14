from django.shortcuts import render
from .models import Product


def all_products(request):
    products = Product.objects.all()  # get all products from the db.
    return render(request, "products/products.html", {"products": products})
