from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from raterapi.views import register_user, login_user, GameView, CategoryView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"games", GameView, "game")
router.register(r"categories", CategoryView, "category")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
