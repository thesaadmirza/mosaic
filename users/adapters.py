from .models import User
from allauth.account.adapter import DefaultAccountAdapter

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = data.get('email')
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_app(self, request, provider):
        # NOTE: Avoid loading models at top due to registry boot...
        from allauth.socialaccount.models import SocialApp

        # 1 added line here
        from allauth.socialaccount import app_settings

        config = app_settings.PROVIDERS.get(provider, {}).get('APP')
        if config:
            app = SocialApp(provider=provider)
            for field in ['client_id', 'secret', 'key']:
                setattr(app, field, config.get(field))

            # 3 added lines here
            app.key = app.key or "unset"
            app.name = app.name or provider
            app.save()

        else:
            app = SocialApp.objects.get_current(provider, request)
        return app

    def pre_social_login(self, request, sociallogin):
        user = User.objects.filter(email=sociallogin.user.email).first()
        if user and not sociallogin.is_existing:
            sociallogin.connect(request, user)
        else:
            return False
