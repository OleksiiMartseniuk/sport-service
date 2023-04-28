from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import CreateUserSerializer


class CreateUserView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
