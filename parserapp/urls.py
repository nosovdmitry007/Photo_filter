from django.urls import path
from parserapp import views

app_name = 'parserapp'

urlpatterns = [
    path('', views.AboutView.as_view(), name='index'),
    path('filterphoto/', views.FilterPhoto.as_view(), name='filterphoto'),
    path('filterfacephoto/', views.FilterFacePhoto.as_view(), name='filterfacephoto'),
    path('indicatfacephoto/', views.IndicatFacePhoto.as_view(), name='indicatfacephoto'),
    path('resultfilter/', views.ResultFilterView.as_view(), name='resultfilter')

]