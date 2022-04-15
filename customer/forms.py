from django import forms
from accounts.models import MyUser
from .models import CompanySeller

class LoginForm(forms.Form):

    email = forms.CharField(label="Почта", widget=forms.EmailInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if MyUser.objects.filter(email=email, banned=True).exists():
            raise forms.ValidationError('Пользователь забанен')
        if not MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого пользователя не существует')
        user = MyUser.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ('email', 'phone', 'first_name', 'last_name', 'avatar')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

    def clean_email(self):
        data = self.cleaned_data
        if MyUser.objects.filter(username=data['email']).exists():
            raise forms.ValidationError('Пользователь с таким названием аккаунта уже существует.')
        return data['email']

class CreateCompanyForm(forms.ModelForm):

    class Meta:
        model = CompanySeller
        fields = ('title', 'phone', 'logo', )

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data['title']
        if CompanySeller.objects.filter(title=title).exists():
            raise forms.ValidationError('Данная компания уже существует')
        return title
