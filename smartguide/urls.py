from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('google/', include('allauth.urls')),
    path('', include('dashboard.urls', namespace='dashboard'))
]
