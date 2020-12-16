from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from .models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=45)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        min_length=settings.MIN_PASSWORD_LENGTH,
        label='Password',
        strip=False,
        help_text=f'Enter {settings.MIN_PASSWORD_LENGTH} digits and chars',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        min_length=settings.MIN_PASSWORD_LENGTH,
        label='Repeat the password',
        strip=False,
        widget=forms.PasswordInput()
    )
    photo = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'photo'
        )

    def crispy_init(self):
        """Initialize crispy-forms helper."""
        self.helper = FormHelper()
        self.helper.form_id = 'id-RegistrationForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('user:api-register')

        self.helper.layout = layout.Layout(
            layout.Field('username'),
            layout.Field('email'),
            layout.Field('password1'),
            layout.Field('password2'),
            layout.Field('photo'),
            layout.Div(
                layout.Submit(
                    'submit',
                    'Register',
                    css_class='btn-success my-2 px-4'
                ),
                css_class='text-center'
            )
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crispy_init()
