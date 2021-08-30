from django.conf.urls import url
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Customer API",
        default_version='v1',
        description="With this API you can Create, Update, View or Remove Customers. You also"
                    "can add a product to a customer's favorite list and view all products in customer's favorite list.",
        contact=openapi.Contact(email="felipe.rayel@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('docs/', include_docs_urls(title='My API title')),
    path("app/", include("api.urls")),
]
