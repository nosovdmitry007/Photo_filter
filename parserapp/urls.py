from django.urls import path
from parserapp import views

app_name = 'parserapp'

urlpatterns = [
    path('', views.AboutView.as_view(), name='index'),
    # path('form/', views.SearchFormView.as_view(), name='form'),
    # path('results/', views.VacancListView.as_view(), name='results'),
    # path('vacancy/<int:id>/', views.VacancyDetailView.as_view(), name='vacancy'),
    # path('comment/<int:pk>/', views.CommentUpdataView.as_view(), name='coment'),
    # path('skil_list/', views.SkillListView.as_view(), name='skil_list'),
    # path('skil_vacanc/<str:skil>/', views.SkilVacDetailView.as_view(), name='skil_vacanc'),
    # path('vac_delite/<int:pk>/', views.VacDeleteView.as_view(), name='vac_delite'),
    path('filterphoto/', views.FilterPhoto.as_view(), name='filterphoto'),
    path('filterfacephoto/', views.FilterFacePhoto.as_view(), name='filterfacephoto'),
    path('resultfilter/', views.ResultFilterView.as_view(), name='resultfilter')

]