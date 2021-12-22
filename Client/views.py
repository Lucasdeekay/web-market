import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets

from Client.models import Client
from .forms import ImageForm
from .serializers import ClientSerializer


def signup(request):
    return render(request, 'client/signup.html')


def submit_signup(request):
    all_clients = Client.objects.all()
    first_name = request.POST['first-name'].strip()
    last_name = request.POST['last-name'].strip()
    gender = request.POST['gender'].strip()
    date_of_birth = request.POST['date-of-birth'].strip()
    email = request.POST['email'].strip()
    phone_number = request.POST['phone-number'].strip()
    address = request.POST['address'].strip()
    if first_name == "" or last_name == "" or gender == "" or date_of_birth == "" or email == "" or phone_number == "" or address == "":
        messages.error(request, 'Fill all boxes')
        return HttpResponseRedirect(reverse('Client:signup'))
    elif all_clients.exists():
        for client in all_clients:
            if email == client.email:
                messages.error(request, "Email already used")
                return HttpResponseRedirect(reverse('Client:signup'))
            elif phone_number == client.phone_number:
                messages.error(request, "Phone Number already used")
                return HttpResponseRedirect(reverse('Client:signup'))
        else:
            Client.objects.create(first_name=first_name, last_name=last_name, gender=gender,
                                  date_of_birth=date_of_birth, email=email, phone_number=phone_number,
                                  address=address)
            return HttpResponseRedirect(reverse('Client:assign-user'))
    else:
        Client.objects.create(first_name=first_name, last_name=last_name, gender=gender,
                              date_of_birth=date_of_birth, email=email, phone_number=phone_number,
                              address=address)
        return HttpResponseRedirect(reverse('Client:assign-user'))


def assign_user(request):
    return render(request, 'client/assign-user.html')


def submit_user(request):
    all_users = User.objects.all()
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm-password']
    last_client = Client.objects.last()

    if username == "":
        messages.error(request, 'Fill in your desired username')
        return HttpResponseRedirect(reverse('Client:assign-user'))
    elif len(password) < 8:
        messages.error(request, "Password must not be less than 8 characters")
        return HttpResponseRedirect(reverse('Client:assign-user'))
    elif len(password) >= 8 and password == confirm_password:
        if all_users.exists():
            for current_user in all_users:
                if current_user.username == username:
                    messages.error(request, "Username already used")
                    return HttpResponseRedirect(reverse('Client:assign-user'))
            else:
                User.objects.create_user(username=username, password=password, email=last_client.email,
                                         first_name=last_client.first_name, last_name=last_client.last_name)
                user = User.objects.get_by_natural_key(username=username)
                Client.objects.filter(id=last_client.id).update(user=user)
                return HttpResponseRedirect(reverse('Client:login'))
        else:
            User.objects.create_user(username=username, password=password, email=last_client.email,
                                     first_name=last_client.first_name, last_name=last_client.last_name)
            user = User.objects.get_by_natural_key(username=username)
            Client.objects.filter(id=last_client.id).update(user=user)
            return HttpResponseRedirect(reverse('Client:login'))
    else:
        messages.error(request, "Password not matched")
        return HttpResponseRedirect(reverse('Client:assign-user'))


def log_in(request):
    return render(request, 'client/login.html')


def submit_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    current_client = get_object_or_404(Client, user=user)
    if user is not None:
        login(request, user=user)
        return HttpResponseRedirect(reverse('Market:homepage', args=(current_client.id,)))
    else:
        messages.error(request, "Username does not exist")
        return HttpResponseRedirect(reverse('Client:login'))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('Client:login'))


def profile(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        return render(request, "client/profile.html", {
            "current_user": current_user,
            "current_client": current_client,
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def change_password(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        return render(request, "client/change-password.html", {
            "current_user": current_user,
            "current_client": current_client
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def reset_password(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if len(password) < 8:
            messages.error(request, "Password must not be less than 8 characters")
            return HttpResponseRedirect(reverse('Client:change-password', args=(client_id,)))
        else:
            if password == confirm_password:
                current_user.set_password(password)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, "Password reset successfully")
                '''send_mail(subject='<h1>Password Change SUCCESSFULLY<h1>',
                          message='Your Webmarket password has been successfully updated',
                          from_email='lucasdeekay@gmail.com',
                          recipient_list=['a.kolawole@dominionuniversity.edu.ng'],
                          fail_silently=False)'''
                return HttpResponseRedirect(reverse('Client:profile', args=(client_id,)))
            else:
                messages.error(request, "Password not matched")
                return HttpResponseRedirect(reverse('Client:change-password', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def edit_profile(request, client_id):
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        return render(request, "client/edit-profile.html", {
            "current_user": current_user,
            "current_client": current_client,
            "imageForm": ImageForm()
        })
    else:
        return HttpResponseRedirect(reverse('Client:login'))


def save_profile(request, client_id):
    if request.user.is_authenticated:
        all_clients = Client.objects.all()
        current_client = get_object_or_404(Client, id=client_id)
        current_user = current_client.user
        first_name = request.POST['first-name'].strip()
        last_name = request.POST['last-name'].strip()
        gender = request.POST['gender'].strip()
        email = request.POST['email'].strip()
        phone_number = request.POST['phone-number'].strip()
        bio = request.POST['bio'].strip()
        image = request.FILES['profile_picture']
        if all_clients.exists():
            for client in all_clients:
                if email != current_client.email and email == client.email:
                    messages.error(request, "Email already used")
                    return HttpResponseRedirect(reverse('Client:edit-profile', args=(client_id,)))
                elif phone_number != current_client.phone_number and phone_number == client.phone_number:
                    messages.error(request, "Phone Number already used")
                    return HttpResponseRedirect(reverse('Client:edit-profile', args=(client_id,)))
            else:
                current_client.first_name = first_name
                current_client.last_name = last_name
                current_client.gender = gender
                current_client.email = email
                current_client.phone_number = phone_number
                current_client.bio = bio

                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.email = email

                if image != "" and current_client.image != "":
                    os.remove(path='media/' + str(current_client.image))
                current_client.image = image
                current_client.save()
                messages.success(request, "Bio successfully edited")
                return HttpResponseRedirect(reverse('Client:profile', args=(client_id,)))
    else:
        return HttpResponseRedirect(reverse('Client:login'))


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('first_name')
    serializer_class = ClientSerializer



