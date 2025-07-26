from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('dashboard/', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('gallery/', include('gallery.urls')),
    path('events/', include('events.urls')),
    path('prayer/', include('prayer.urls')),
    path('jobs/', include('jobs.urls')),
    path('mentorship/', include('mentorship.urls')),
    path('resources/', include('resources.urls')),
    path('history/', include('history.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
