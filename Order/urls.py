from django.urls import path, include
from Order import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('order', views.OrderViewSet)

app_name = 'Order'

urlpatterns = [
    path('<int:client_id>/<str:category_name>/<str:product_name>/add_to_cart', views.add_to_cart, name="add-to-cart"),
    path('cart/<int:client_id>/', views.cart, name="cart"),
    path('cart/<int:client_id>/payment', views.payment, name="payment"),
    path('cart/<int:client_id>/make_order/<int:order_id>/', views.make_order, name="make-order"),
    path('cart/<int:client_id>/cancel_order/<int:order_id>/', views.cancel_order, name="cancel-order"),
    path('cart/<int:client_id>/delete_order/<int:order_id>/', views.delete_order, name="delete-order"),
    path('order-api', include(router.urls)),
]