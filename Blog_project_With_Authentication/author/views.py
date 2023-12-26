from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from posts.models import Post

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Register Successfully.')
            return redirect('profile ')
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html',{'form':register_form, 'type':'Register'})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password = user_pass)
            if user is not None:
                login(request, user)
                messages.success(request,'Login Successfylly.')
                return redirect('profile')
            else:
                messages.warning(request, 'Login Information Is Incorrenct')
                return redirect('profile')
            
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form':form, 'type':'Login'})


@login_required
def user_profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, 'user_profile.html',{'data':data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChageUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully.')
            return redirect('register')
    else:
        profile_form = forms.ChageUserForm(instance=request.user)
    return render(request, 'update_profile.html',{'form':profile_form})


def pass_change(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully.')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('user_longin')