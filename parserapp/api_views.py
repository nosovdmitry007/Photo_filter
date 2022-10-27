from .models import Skills_table, Vacancy
from .serializers import SkilsSerializer, VacancySerializer
from rest_framework import viewsets

class SkilsViewSet(viewsets.ModelViewSet):
    queryset = Skills_table.objects.all()
    serializer_class = SkilsSerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer