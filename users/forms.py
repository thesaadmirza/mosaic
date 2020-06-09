from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.utils.translation import ugettext_lazy as _




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

