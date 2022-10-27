from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import  PhotoFilterForm, PhotoFaceFilterForm
from django.views.generic import TemplateView
from .PhotoFilter import filterphoto
from django.views.generic.edit import FormView
from .face_detection import face_filter

#главная страница
class AboutView(TemplateView):
    template_name = "parserapp/index.html"


class FilterPhoto(LoginRequiredMixin,FormView):
    template_name = 'parserapp/filterphoto.html'
    form_class = PhotoFilterForm
    success_url = reverse_lazy('parserapp:resultfilter')

    def form_valid(self, form):
        put = form.cleaned_data['put']
        format = form.cleaned_data['format']
        filterphoto(put,format)

        return super().form_valid(form)



class FilterFacePhoto(LoginRequiredMixin,FormView):
    template_name = 'parserapp/filterfacephoto.html'
    form_class = PhotoFaceFilterForm
    success_url = reverse_lazy('parserapp:resultfilter')

    def form_valid(self, form):
        put = form.cleaned_data['put']
        # format = form.cleaned_data['format']
        face_filter(put)

        return super().form_valid(form)

class ResultFilterView(TemplateView):
    template_name = "parserapp/resultfilter.html"