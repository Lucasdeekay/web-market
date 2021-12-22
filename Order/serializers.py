from rest_framework import serializers

from Order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'product', 'quantity', 'total_cost', 'date', 'time', 'status')
