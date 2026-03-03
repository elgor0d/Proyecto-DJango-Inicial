from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from urllib.parse import urlparse
from datetime import datetime


def login_view(request):

    # Si ya está autenticado, no tiene caso mostrar el login
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin:index")
        return redirect("user_panel")

    next_url = request.GET.get('next')

    if request.method == "POST":

        # ✅ Se pasa directo sin guardar la contraseña en variables extra
        username = request.POST.get("username", "").strip()

        # Evita procesar si los campos están vacíos
        if not username or not request.POST.get("password", ""):
            messages.error(request, "Por favor completa todos los campos.")
            return render(request, "accounts/login.html")

        user = authenticate(
            request,
            username=username,
            password=request.POST.get("password", "")  # ✅ Sin variable extra
        )

        if user:
            login(request, user)

            # ✅ Solo guarda datos no sensibles en la sesión
            request.session['ultimo_acceso'] = str(datetime.now())

            # Validar que next_url sea una ruta interna (evita Open Redirect)
            if next_url:
                parsed = urlparse(next_url)
                if not parsed.netloc and not parsed.scheme:
                    return redirect(next_url)

            if user.is_superuser:
                return redirect("admin:index")

            return redirect("user_panel")

        messages.error(request, "Credenciales incorrectas.")

    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":

        # ✅ Limpia datos sensibles de la sesión antes de cerrar
        request.session.pop('ultimo_acceso', None)
        request.session.flush()  # ✅ Elimina toda la sesión de la memoria

        logout(request)
        return redirect("login")
    return redirect("user_panel")


@login_required(login_url="/")
def admin_panel(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder aquí.")
    return render(request, "dashboard/admin_panel.html")


@login_required(login_url="/")
def user_panel(request):
    return render(request, "dashboard/alumno.html", {
        "user": request.user
    })