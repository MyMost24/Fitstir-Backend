from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from backend import urls
from backend import views as backendViews 
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include(urls.urlpatterns)),
                  path('backend/',include(urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

