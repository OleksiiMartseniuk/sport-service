from rest_framework import generics

from .models import Category
from .serializers import CategorySerializers


class CategoryView(generics.ListAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all()
