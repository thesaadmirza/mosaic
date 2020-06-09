from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.utils.translation import ugettext_lazy as _
from django import forms
from users.models import User, Customer


class MyCustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['password'].label = False
        self.fields['login'].label = False
        self.helper.add_input(Submit('submit', _('Login'), css_class="form-control btn btn-login"))

    def login(self, *args, **kwargs):
        # Add your own processing here.
        user = super(MyCustomLoginForm, self).login(*args, **kwargs)
        # You must return the original result.
        return user


class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].help_text = _('Password Instructions')
        self.helper.add_input(Submit('submit', _('Sign Up'), css_class="form-control btn btn-login"))

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        user.type = "S"
        user.save()
        # Add your own processing here.
        # You must return the original result.
        return user


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'phone']
