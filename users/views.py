import os
from django.db import models
import requests
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from . import forms, models as user_models



class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        print("CSRF")
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
                
        return render(request, "users/login.html", context={"form": form})
        

def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))

class SignUpView(FormView):
    
    template_name = "users/signup.html"
    form_class= forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        user.save()
        return super().form_valid(form)


def complite_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
        return redirect(reverse("core:home"))
    except user_models.User.DoesNotExist:
        # to do: add error message
        pass


class GithubException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        code = request.GET.get("code", None)
        client_secret = os.environ.get("GH_SECRET")
        if code is None:
            raise GithubException("code is None")
        token_request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}", 
            headers={"Accept": "application/json"}
            )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise GithubException("Can't get access token")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json"
            },
        )
        profile_json: dict = profile_request.json()
        username = profile_json.get("login", None)
        if username is None:
            raise GithubException("username is None")
        print(profile_json)
        email = profile_json.get("email")
        if email is None:
            raise GithubException("Your github account does not have public email.")
        first_name = profile_json.get("name")
        if first_name is None:
            first_name=""
        bio = profile_json.get("bio")
        if bio is None:
            bio = ""

        try:
            user = user_models.User.objects.get(email=email)
            if user_models.User.LOGIN_GITHUB not in user.login_method:
                raise GithubException(f"User with email={email} - can not log in by Github."+
                    "If you want to link accounts - you shoul login and configure your login methods."
                )
        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                username=email, first_name=first_name, bio=bio,
                email=email, email_verified=True,
                login_method=user_models.User.LOGIN_GITHUB
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("core:home"))
    except GithubException as e:
        print(e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def kakao_login(request):
    api_key = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={api_key}&redirect_uri={redirect_uri}&response_type=code")


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kaccount_email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException(
                    f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
