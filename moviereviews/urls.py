from django.contrib import admin
from django.urls import path, include
from movie import views as movieViews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('movie.urls')),
    path('news/', include('news.urls')),

    path('statistics/', movieViews.statistics_view, name='statistics'),

    # ✅ esto habilita el link del navbar
    path('signup/', movieViews.signup, name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)