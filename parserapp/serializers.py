from django.urls import path, include
from .models import Skills_table,Vacancy
from rest_framework import routers, serializers, viewsets

class SkilsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skills_table
        exclude = ['user']

class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacancy
        skils = SkilsSerializer(many=True)
        exclude = ['user']