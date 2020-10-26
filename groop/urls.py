from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gerver.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls')),
]
