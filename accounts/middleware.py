from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden


class AdminAccessMiddleware:

    RUTAS_PUBLICAS = ['/', '/login/', '/logout/']  # ✅ Agrega login y logout

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ── Protección del panel /admin ──────────────────────
        if request.path.startswith("/admin"):
            if not request.user.is_authenticated:
                return redirect("login")
            if not request.user.is_superuser:
                return HttpResponseForbidden("Acceso denegado.")

        # ── Protección general ────────────────────────────────
        ruta_publica = any(
            request.path == ruta for ruta in self.RUTAS_PUBLICAS
        )

        if not ruta_publica and not request.user.is_authenticated:
            return redirect('/')  # ✅ Redirige al login (ruta raíz)

        response = self.get_response(request)
        return response
    
    def __call__(self, request):
        response = self.get_response(request)
    
        # ✅ Elimina el header que expone la versión del servidor
        response.headers.pop('Server', None)
        response.headers.pop('X-Powered-By', None)
    
        return response
