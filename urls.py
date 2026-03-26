from django.contrib import admin
from django.urls import path, include # Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # This connects everything you wrote in core/urls.py to the root website
    path('', include('core.urls')), 
]