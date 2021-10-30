from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    # Local apps
    path(
        'healthcheck/',
        include(
            ('wimpy.healthcheck.urls', 'healthcheck'),
            namespace='healthcheck'
        )
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    # 3rd party apps
    path(
        'api/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
