from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('charities/', include('charities.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('about_us.urls')),
]
