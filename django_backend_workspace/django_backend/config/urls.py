"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as drf_status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# --- Swagger Schema Definitions for /api/count ---

# Blank line fix for E302 (two blank lines before top-level class)


class CountRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        help_text="Text for which word and character counts will be computed.",
        required=True,
        example="Hello world"
    )


class CountResponseSerializer(serializers.Serializer):
    word_count = serializers.IntegerField(
        help_text="Number of words in input text."
    )
    character_count = serializers.IntegerField(
        help_text="Number of characters in input text."
    )


@swagger_auto_schema(
    method="post",
    operation_description="Count words and characters in submitted text.",
    operation_summary="Compute word and character counts",
    request_body=CountRequestSerializer,
    responses={
        200: openapi.Response("Successful response", CountResponseSerializer),
        400: "Bad Request: Invalid or missing 'text' field"
    },
    tags=["Count"],
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def count_doc_view(request):
    """
    Count words and characters in the submitted text.

    POST body:
    {
      "text": "your string here"
    }

    Response:
    {
      "word_count": int,
      "character_count": int
    }
    """
    serializer = CountRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"error": "Field 'text' must be a string."},
            status=drf_status.HTTP_400_BAD_REQUEST
        )
    text = serializer.validated_data["text"]
    words = text.split()
    return Response({
        "word_count": len(words),
        "character_count": len(text)
    })


schema_view = get_schema_view(
    openapi.Info(
        title="Word/Char Count API",
        default_version='v1',
        description=(
            "API to count words and characters in input text. \n\nPOST `/api/count/` "
            "with `{ \"text\": \"your string\" }` to get word and character counts."
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/count-docs/', count_doc_view, name='count-doc-view'),
        # include the rest of the API for docs:
        path('api/', include('api.urls')),
    ],
)

urlpatterns += [
    # Main API doc UI
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger\.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Add a dedicated count endpoint example to schema for /api/count-docs/
    path('api/count-docs/', count_doc_view, name='count-doc-view'),
]
