from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions


# PUBLIC_INTERFACE
@api_view(['GET'])
def health(request):
    """Health check endpoint, returns server status."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def count(request):
    """
    POST /api/count
    Computes word and character counts for input text.
    ---
    request body:
        { "text": "<string>" }
    response:
        { "word_count": <int>, "character_count": <int> }
    """
    data = request.data
    text = data.get('text', '')
    if not isinstance(text, str):
        return Response(
            {"error": "Field 'text' must be a string."},
            status=status.HTTP_400_BAD_REQUEST
        )
    words = text.split()
    word_count = len(words)
    character_count = len(text)
    return Response({
        "word_count": word_count,
        "character_count": character_count
    })
