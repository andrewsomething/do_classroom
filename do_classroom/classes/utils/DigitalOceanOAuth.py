from social.backends.oauth import BaseOAuth2

from ..models import Teacher

class DigitalOceanOAuth(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'digitalocean'
    AUTHORIZATION_URL = 'https://cloud.digitalocean.com/v1/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://cloud.digitalocean.com/v1/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = [
        ('expires_in', 'expires_in')
    ]

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response['account'].get('uuid')

    def get_user_details(self, response):
        """Return user details from DigitalOcean account"""
        return {'username': response['account'].get('uuid'),
                'email': response['account'].get('email'),
                'full_name': response['account'].get('name') or ''}

    def user_data(self, token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.digitalocean.com/v2/account'
        auth_header = {"Authorization" : "Bearer %s"  % token}
        try:
            return self.get_json(url, headers=auth_header)
        except ValueError:
            return None


def save_account(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'digitalocean':
        if is_new:
            teacher, created = Teacher.objects.get_or_create(user=user,
                                    email=response['account'].get('email'),
                                    uuid=response['account'].get('uuid'),
                                    droplet_limit=response['account'].get('droplet_limit'))
        else:
            teacher = Teacher.objects.get(user=user)
            teacher.email = response['account'].get('email')
            teacher.droplet_limit = response['account'].get('droplet_limit')
            teacher.save()