from django.shortcuts import render
from rest_framework import viewsets

from .models import ApiData
from .serializers import ApiDataSerializer
# Create your views here.


class ApiDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows API data to be viewed.
    """
    queryset = ApiData.objects.all().order_by('-created_at')
    serializer_class = ApiDataSerializer

