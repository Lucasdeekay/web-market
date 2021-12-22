from django.urls import path
from Market import views

app_name = 'Market'

urlpatterns = [
    path('<int:client_id>', views.index, name='homepage'),
]