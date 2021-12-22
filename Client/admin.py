from django.contrib import admin
from Client.models import Client, User


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone_number', 'address', 'bio', 'image')


admin.site.register(Client, ClientAdmin)
