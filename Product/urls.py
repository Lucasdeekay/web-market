from django.urls import path, include
from Product import views
from rest_framework import routers

app_name = 'Product'

router = routers.DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('category', views.CategoryViewSet)

urlpatterns = [
    path('<int:client_id>', views.store, name='store'),
    path('<int:client_id>/<str:category_name>', views.product_store, name='product-store'),
    path('<int:client_id>/<str:category_name>/<str:product_name>', views.individual_product, name='individual-product'),
    path('product-api', include(router.urls)),
]