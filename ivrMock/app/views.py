from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlparse, parse_qs
from .tasks import process_mocked_call


@api_view(['POST'])
def token_obtain(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access_token': str(refresh.access_token),
    }, status=200)


@api_view(['POST'])
def outbound_calls(request):
    data = request.data

    event_url = data["event_url"][0]
    parsed_url = urlparse(event_url)
    path_parts = parsed_url.path.split('/')

    # Extract internal.callId from the URL path
    internal_call_id = path_parts[-1]

    # Extract conversation_uuid from the query parameters
    query_params = parse_qs(parsed_url.query)
    conversation_uuid = query_params.get('externalIdParamName')[0]

    # Create a mock response
    response_data = {
        "uuid": internal_call_id,
        "status": "completed",
        "direction": "outbound",
        "conversation_uuid": f"CON-{conversation_uuid}",
    }

    process_mocked_call.delay(data, response_data)

    return Response(response_data)
