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
                  path('backend/', include(urls)),
                  path('rest-auth/', include('rest_auth.urls')),
                  # path('rest-auth/registration/', include('rest_auth.registration.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
