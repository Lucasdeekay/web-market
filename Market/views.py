from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Client.models import User, Client


def index(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        return render(request, 'market/index.html', {
            "current_user": current_user,
            "current_client": current_client
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))



