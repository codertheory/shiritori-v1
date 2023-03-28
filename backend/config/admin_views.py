from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status


@ensure_csrf_cookie
def set_csrf_token(request: ASGIRequest):
    """
    This will be `/api/set-csrf-cookie/` on `urls.py`
    """
    if not request.session.session_key:
        request.session.save(must_create=True)
    return JsonResponse({"details": "CSRF cookie set"}, status=status.HTTP_200_OK)


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
