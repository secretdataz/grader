from rest_framework import viewsets

from .models import *
from .serializers import *

class TestViewSet(viewsets.ModelViewSet):
	queryset = Test.objects.all()
	serializer_class = TestSerializer

class ProblemViewSet(viewsets.ModelViewSet):
	queryset = Problem.objects.all()
	serializer_class = ProblemSerializer
