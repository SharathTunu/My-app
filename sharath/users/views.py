from users.models import CustomUser
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm
from rest_framework import viewsets
from rest_framework.response import Response

from .serializer import RegistrationSerializer

# Create your views here.

class RegistrationViewSet(viewsets.ModelViewSet):
    
    queryset = CustomUser.objects.none()
    serializer_class = RegistrationSerializer

    def get(self, *args, **kwargs):
        print("Hello!")
        form = UserRegistration()

        context = {
            "form": form
        }
        return render(request, 'users/register.html', context=context)

    def post(self, *args, **kwargs):
        self.request.data

@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'users/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'users/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'users/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'users/edit.html', context=context)