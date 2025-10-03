from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tests/', include('tests.urls')),
    path('', include('core.urls')),  # homepage
]
