from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm


def user_login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form': login_form})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse('Wellcom You. You have logined the website.')
            else:
                return HttpResponse('Sorry, Your username or password is not right.')
        else:
            return HttpResponse('Invalid login.')


def register(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()   # new
        return render(request, 'account/register.html', {'form': user_form, 'profile': userprofile_form})   # new
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)  # new
        if user_form.is_valid() * userprofile_form.is_valid():   # new
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # new
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse('恭喜，注册成功了。')
        else:
            return HttpResponse('Sorry，注册失败了。')