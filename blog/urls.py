
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rms.views import ResultView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path("result-management-system/", ResultView.as_view(),
         name="result-management-system")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
