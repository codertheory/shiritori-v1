from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from shiritori.game.views import GameViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register('game', GameViewSet, basename='game')

app_name = "api"
urlpatterns = router.urls
