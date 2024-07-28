from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.views.static import serve
from src.website.views import handler404


handler404 = handler404

urlpatterns = [
    # REQUIRED --------------------------------------------------------- #
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('', include('src.website.urls', namespace='website')),
    path('a/', include('src.portals.admins.urls', namespace='admins')),
path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
    
    
    path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)