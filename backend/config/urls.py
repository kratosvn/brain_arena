"""
URL configuration for Brain Arena project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/games/', include('apps.games.urls')),
    path('api/shop/', include('apps.shop.urls')),
    path('api/ai/', include('apps.ai.urls')),
    path('api/pvp/', include('apps.pvp.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'Đấu Trường Tri Thức - Admin'
admin.site.site_title = 'Brain Arena Admin'
admin.site.index_title = 'Quản Lý Hệ Thống'
