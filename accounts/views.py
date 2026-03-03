from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


def login_view(request):

    # Si ya está autenticado, no tiene caso mostrar el login
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin:index")
        return redirect("user_panel")

    next_url = request.GET.get('next')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Evita procesar si los campos están vacíos
        if not username or not password:
            messages.error(request, "Por favor completa todos los campos.")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Validar que next_url sea una ruta interna (evita Open Redirect)
            if next_url:
                parsed = urlparse(next_url)
                if not parsed.netloc and not parsed.scheme:  # Es ruta relativa
                    return redirect(next_url)

            if user.is_superuser:
                return redirect("admin:index")

            return redirect("user_panel")

        messages.error(request, "Credenciales incorrectas.")

    return render(request, "accounts/login.html")


def logout_view(request):
    # Solo permitir logout por POST evita cerrar sesión con un simple enlace
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("user_panel")  # GET al logout no hace nada


@login_required(login_url="/")
def admin_panel(request):
    if not request.user.is_superuser:
        # 403 en lugar de redirigir, evita que usuarios prueben rutas de admin
        return HttpResponseForbidden("No tienes permiso para acceder aquí.")

    return render(request, "dashboard/admin_panel.html")


@login_required(login_url="/")
def user_panel(request):
    # Pasar el usuario al template para mostrar sus datos de forma segura
    return render(request, "dashboard/alumno.html", {
        "user": request.user
    })