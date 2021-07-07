from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import logout
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# def home(request):
#     return render(request, 'users/../articles/templates/articles/home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!!')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


# class LoginAfterPasswordChangeView(PasswordChangeView):
#     @property
#     def success_url(self):
#         return reverse_lazy('login')
#
# login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })


# def home(request):
#     return render(request, 'users/../articles/templates/articles/home.html')


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)