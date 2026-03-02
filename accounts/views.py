from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages


def login_view(request):

    next_url = request.GET.get('next')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,
                            username=username,
                            password=password)

        if user:
            login(request, user)


            if next_url:
                return redirect(next_url)

            if user.is_superuser:
                return redirect("admin:index")

            return redirect("user_panel")

        messages.error(request, "Credenciales incorrectas")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect("user_panel")

    return render(request, "accounts/admin_panel.html")


@login_required
def user_panel(request):
    return render(request, "accounts/user_panel.html")