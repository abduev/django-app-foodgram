from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken'),),
    path('api/users/', include('users.urls')),
    path('api/', include('api.urls'))
]
