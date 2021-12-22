from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets

from Client.models import Client
from Product.models import Category, Product
from Product.serializers import CategorySerializer, ProductSerializer


def store(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        all_categories = Category.objects.all()
        return render(request, 'product/store.html', {
            "current_user": current_user,
            "current_client": current_client,
            "all_categories": all_categories,
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def product_store(request, client_id, category_name):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        category = get_object_or_404(Category, name=category_name)
        all_products = Product.objects.filter(category=category)
        return render(request, 'product/product-store.html', {
            "current_user": current_user,
            "current_client": current_client,
            "category": category,
            "all_products": all_products,
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def individual_product(request, client_id, category_name, product_name):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        category = get_object_or_404(Category, name=category_name)
        product = get_object_or_404(Product, name=product_name)
        return render(request, 'product/individual-product.html', {
            "current_user": current_user,
            "current_client": current_client,
            "category": category,
            "product": product,
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
