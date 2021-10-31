from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    # Local apps
    path(
        '',
        RedirectView.as_view(
            permanent=False,
            url=reverse_lazy('admin:login')
        )
    ),
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
    path(
        'events/',
        include(
            ('wimpy.events.urls', 'events'),
            namespace='events'
        )
    ),
    # 3rd party apps
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'docs/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
