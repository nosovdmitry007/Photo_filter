from django import forms

class PhotoFilterForm(forms.Form):
    form = (('jpg', 'JPG'),
            ('jpeg', 'JPEG'),
            ('cr', 'Kodak: CR'),
            ('k25', 'Kodak: K25'),
            ('kdc', 'Kodak: KDC'),
            ('crw', 'Canon: CRW'),
            ('cr2', 'Canon: CR2'),
            ('cr3', 'Canon: CR3'),
            ('erf', 'Epson: ERF'),
            ('nef', 'Nikon: NEF'),
            ('nrw', 'Nikon: NRW'),
            ('orf', 'Olympus: ORF'),
            ('pef', 'Pentax: PEF'),
            ('rw2', 'Panasonic: RW2'),
            ('arw', 'Sony: ARW'),
            ('srf', 'Sony: SRF'),
            ('sr2', 'Sony: SR2'))
    put = forms.CharField(label='Путь к папке с фотографиями',widget=forms.TextInput(attrs={'placeholder': 'Путь', 'class': 'form-control'}))
    format = forms.ChoiceField(choices=form, label='Расширение файлов',widget=forms.Select(attrs={'class': 'form-control'}))

class PhotoFaceFilterForm(forms.Form):

    put = forms.CharField(label='Путь к папке с фотографиями',widget=forms.TextInput(attrs={'placeholder': 'Путь', 'class': 'form-control'}))
    # format = forms.ChoiceField(choices=form, label='Расширение файлов',widget=forms.Select(attrs={'class': 'form-control'}))

