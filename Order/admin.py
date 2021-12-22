from django.contrib import admin

from Order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_cost', 'date', 'time', 'status')


admin.site.register(Order, OrderAdmin)
