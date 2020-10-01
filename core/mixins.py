class SocialLoginRequiredMixin():
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        try:
            if (request.user.social_auth.exists()):
                print("Social Account Exist*******************************")
        except Exception as e:
            print(e)
        return True
