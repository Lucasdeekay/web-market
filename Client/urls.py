from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Client import views
from rest_framework import routers
from .views import ClientViewSet

app_name = 'Client'

router = routers.DefaultRouter()
router.register('client', ClientViewSet)

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/submit/', views.submit_signup, name='submit-signup'),
    path('signup/assign-user/', views.assign_user, name='assign-user'),
    path('signup/submit-user/', views.submit_user, name='submit-user'),
    path('', views.log_in, name='login'),
    path('login/submit/', views.submit_login, name='submit-login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/<int:client_id>', views.profile, name='profile'),
    path('profile/change-password/<int:client_id>', views.change_password, name='change-password'),
    path('profile/change-password/reset/<int:client_id>', views.reset_password, name='reset-password'),
    path('profile/edit-profile/<int:client_id>', views.edit_profile, name='edit-profile'),
    path('profile/save-profile/<int:client_id>', views.save_profile, name='save-profile'),
    path('client-api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
