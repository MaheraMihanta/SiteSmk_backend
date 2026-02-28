from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserRole
from .serializers import LoginSerializer, UserSerializer

User = get_user_model()


class MeView(APIView):
    def get(self, request):
        if request.user.role == UserRole.ADMIN:
            return Response(
                {'detail': 'Kaonty mpitantana: ampiasao ny sehatra /admin.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].strip().lower()
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email__iexact=email, is_active=True)
        except User.DoesNotExist:
            return Response({'detail': 'Diso ny email na teny miafina.'}, status=status.HTTP_401_UNAUTHORIZED)

        authenticated_user = authenticate(request=request, username=user.username, password=password)
        if not authenticated_user:
            return Response({'detail': 'Diso ny email na teny miafina.'}, status=status.HTTP_401_UNAUTHORIZED)

        if authenticated_user.role == UserRole.ADMIN:
            return Response(
                {'detail': 'Kaonty mpitantana: ampiasao ny sehatra /admin.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(authenticated_user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(authenticated_user).data,
            },
            status=status.HTTP_200_OK,
        )
