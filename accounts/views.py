from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from boards.models import Result
from django.shortcuts import render, redirect
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            result = Result(user=user, sop_instance_uid='1.2.3.4.5', tests='MG', results='Good')
            result.save()
            result = Result(user=user, sop_instance_uid='5.4.3.2.1', tests='MG', results='Inframammary fold')
            result.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})