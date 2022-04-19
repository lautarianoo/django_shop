from django import forms
from .models import ApplyOrganization

class ApplyOrganizationForm(forms.ModelForm):

    class Meta:
        model = ApplyOrganization
        exclude = ('accepted', 'no_accepted', )

    def clean(self, *args , **kwargs):
        data = self.cleaned_data
        if ApplyOrganization.objects.filter(name_organization=data['name_organization']).exists():
            raise forms.ValidationError("Заявка на эту организацию уже подана")
        return self.cleaned_data

class AdminEditApplicationForm(forms.Form):

    text_admin = forms.CharField(label="Текст для заявки", widget=forms.Textarea())
    accept = forms.BooleanField(label="Принять")
    no_accept = forms.BooleanField(label="Отклонить")
