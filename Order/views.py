from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets


# Create your views here.
from django.urls import reverse

from Client.models import User, Client
from Order.models import Order
from Order.serializers import OrderSerializer
from Product.models import Product


def add_to_cart(request, client_id, category_name, product_name):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        product = get_object_or_404(Product, name=product_name)
        quantity = request.POST["quantity"].strip()
        if quantity == '' or int(quantity) < 1:
            messages.error(request, "Please enter a valid quantity")
            return HttpResponseRedirect(reverse('Product:individual-product', args=(client_id, category_name, product_name)))
        elif int(quantity) > product.stock:
            messages.error(request, "Quantity is greater than current stock")
            return HttpResponseRedirect(
                reverse('Product:individual-product', args=(client_id, category_name, product_name)))
        else:
            total_cost = product.price * int(quantity)
            order_date = datetime.now().date()
            order_time = datetime.now().time()
            product.stock -= int(quantity)
            product.save()
            Order.objects.create(user=current_user, product=product, quantity=int(quantity), total_cost=total_cost, date=order_date, time=order_time)
            messages.success(request, "Order successfully made")
            return HttpResponseRedirect(reverse('Product:store', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def cart(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        current_user_orders = Order.objects.filter(user=current_user).order_by("-date")
        return render(request, 'order/cart.html', {
            "current_user": current_user,
            "current_client": current_client,
            "current_user_orders": current_user_orders
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def make_order(request, client_id, order_id):
    if request.user.is_authenticated:
        current_order = get_object_or_404(Order, id=order_id)
        product_ordered = current_order.product
        current_order.status = True
        current_order.save()
        messages.success(request, f"Order for {product_ordered} successfully")
        return HttpResponseRedirect(reverse('Order:cart', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def cancel_order(request, client_id, order_id):
    if request.user.is_authenticated:
        current_order = get_object_or_404(Order, id=order_id)
        product_ordered = current_order.product
        current_order.status = False
        current_order.save()
        messages.success(request, f"Order for {product_ordered} cancelled")
        return HttpResponseRedirect(reverse('Order:cart', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def delete_order(request, client_id, order_id):
    if request.user.is_authenticated:
        current_order = get_object_or_404(Order, id=order_id)
        product_ordered = current_order.product
        product_ordered.stock += current_order.quantity
        product_ordered.save()
        current_order.delete()
        messages.error(request, f"Order for {product_ordered} deleted")
        return HttpResponseRedirect(reverse('Order:cart', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def payment(request, client_id):
    def get_total_amount(orders):
        total = 0
        for order in orders:
            total += order.total_cost
        return total

    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        current_user_orders = Order.objects.filter(user=current_user, status=True)
        total_amount = get_total_amount(current_user_orders)
        return render(request, 'order/payment.html', {
            "current_user": current_user,
            "current_client": current_client,
            "current_user_orders": current_user_orders,
            "total_amount": total_amount
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer

