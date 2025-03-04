from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    re_path,
    path,
)
from django.views.generic import RedirectView

from app.misc.views import healthcheck
from app.misc.views import LandingPageView

from .routers import v1_urls


schema_view = get_schema_view(
    openapi.Info(
        title='olie',
        default_version='v1',
        description='olie',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_patterns = [
    re_path(
        r'api(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json-yaml',
    ),
    path(
        'api/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger',
    ),
]

jwt_patterns = [
    path('api/v1/token/', obtain_jwt_token),
    path('api/v1/token/refresh/', refresh_jwt_token),
    path('api/v1/token/verify/', verify_jwt_token),
]

patterns = [
    path('healthcheck/', healthcheck, name='healthcheck'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1_urls)),
    path('questions/', include('app.questions.urls')),
    path('', LandingPageView.as_view(), name='index'),
]

urlpatterns = schema_patterns + jwt_patterns + patterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
