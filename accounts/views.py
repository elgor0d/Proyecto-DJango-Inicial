from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,
                            username=username,
                            password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_panel")
            else:
                return redirect("user_panel")

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