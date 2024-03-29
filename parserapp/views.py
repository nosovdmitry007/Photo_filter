from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PhotoFilterForm, PhotoFaceFilterForm, Face_indetefic
from django.views.generic import TemplateView
from .PhotoFilter import filterphoto
from django.views.generic.edit import FormView
from .person_detect import YOLO_filter
from .closes_eyes import closes_eyes
from .face_indetecation import face_inc
yolo = YOLO_filter()
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
        wath = form.cleaned_data['wath']
        print(wath)
        if wath == 'quality':
            filterphoto(put,format)
        elif wath == 'eyes':
            print('\n tfdch\n')
            closes_eyes(put, format)

        return super().form_valid(form)


class FilterFacePhoto(LoginRequiredMixin,FormView):
    template_name = 'parserapp/filterfacephoto.html'
    form_class = PhotoFaceFilterForm
    success_url = reverse_lazy('parserapp:resultfilter')

    def form_valid(self, form):

        put = form.cleaned_data['put']
        format = form.cleaned_data['format']
        cat = form.cleaned_data['cat']
        yolo.person_filter(put, format, cat)
        return super().form_valid(form)


class IndicatFacePhoto(LoginRequiredMixin,FormView):
    template_name = 'parserapp/indicatfacephoto.html'
    form_class = Face_indetefic
    success_url = reverse_lazy('parserapp:resultfilter')

    def form_valid(self, form):
        put_face = form.cleaned_data['put_face']
        # format = form.cleaned_data['format']
        put_photo = form.cleaned_data['put_photo']
        face_inc(put_face, put_photo)

        return super().form_valid(form)


class ResultFilterView(TemplateView):
    template_name = "parserapp/resultfilter.html"