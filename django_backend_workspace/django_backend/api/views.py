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

    Expects JSON body:
        { "text": "<string>" }
    Returns:
        { "word_count": <int>, "character_count": <int> }

    Returns 400 if 'text' is missing or is not a string.
    """
    # Ensure we are receiving a JSON payload with the correct content type
    if not request.content_type.startswith('application/json'):
        return Response(
            {"error": "Content-Type must be application/json."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        data = request.data
    except Exception:
        return Response(
            {"error": "Invalid JSON body."},
            status=status.HTTP_400_BAD_REQUEST
        )
    text = data.get('text', None)

    if text is None:
        return Response(
            {"error": "Field 'text' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not isinstance(text, str):
        return Response(
            {"error": "Field 'text' must be a string."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Strip leading/trailing whitespace to ensure word/char count matches intent
    text_stripped = text.strip()
    words = text_stripped.split()
    word_count = len(words)
    character_count = len(text_stripped)

    return Response({
        "word_count": word_count,
        "character_count": character_count
    })
