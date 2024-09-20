from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')), 
    path('api/chat/', include('base.chat.urls')),
]
