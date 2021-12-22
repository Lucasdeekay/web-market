from django.contrib import admin

from Product.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'stock')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
