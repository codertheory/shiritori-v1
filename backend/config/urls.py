from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import status

urlpatterns = [
                  # Your stuff: custom urls includes go here
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()


@ensure_csrf_cookie
def set_csrf_token(request: ASGIRequest):
    """
    This will be `/api/set-csrf-cookie/` on `urls.py`
    """
    if not request.session.session_key:
        request.session.save(must_create=True)
    return JsonResponse({"details": "CSRF cookie set"}, status=status.HTTP_200_OK)


def health_check(request: ASGIRequest):
    """
    This will be `/health/` on `urls.py`
    """
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)


def load_dictionary_view(request: ASGIRequest):
    """
    This will be `/load-dictionary/` on `urls.py`
    """
    key = request.GET.get("key")
    locale = request.GET.get("locale", "en")
    if key != settings.LOAD_DICTIONARY_KEY:
        return JsonResponse({"status": "error"}, status=status.HTTP_403_FORBIDDEN)
    from shiritori.game.tasks import load_dictionary_task
    load_dictionary_task.delay(locale)
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)


# API URLS
urlpatterns += [
    # API base url
    path("health/", health_check, name="health-check"),
    path("api/", include("config.api_router")),
    path("api/set-csrf-cookie/", set_csrf_token, name="set-csrf-cookie"),
    path("api/load-dictionary/", load_dictionary_view, name="load-dictionary"),
    # DRF auth token
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]
