from django.shortcuts import render, redirect
from restaurant_auth.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def signup(request):
    registered = False
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            registered = True
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(
        request, 'restaurant_auth/signup.html',
        {'form': form, 'registered': registered}
    )


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('search:search'))
            else:
                return render(
                    request, 'restaurant_auth/login.html',
                    {'error': 'Your account is marked inactive.'}
                )
        else:
            return render(
                request, 'restaurant_auth/login.html',
                {'error': 'Invalid login credentials'}
            )
    else:
        return render(request, 'restaurant_auth/login.html', {})


@login_required
def signout(request):
    logout(request)
    return redirect(reverse('restaurant_auth:login'))
