from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from users.views import UserCustomViewSet

router = DefaultRouter()
router.register(r'', UserCustomViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
