from allauth.socialaccount.models import SocialToken

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except Exception as e:
    print("Error importing Google APi CLient")


def get_calendar_service(request):
    social_token = SocialToken.objects.filter(account__user=request.user, account__provider='google').latest('id')
    creds = Credentials(token=social_token.token,
                        refresh_token=social_token.token_secret,
                        client_id=social_token.app.client_id,
                        client_secret=social_token.app.secret)
    service = build('calendar', 'v3', credentials=creds)
    return service
