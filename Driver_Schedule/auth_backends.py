from django.contrib.auth.models import User , Group
from django.contrib.auth.backends import ModelBackend



class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, db_name = None, **kwargs):
        user = User.objects.using(db_name).get(username=username)
        if user.check_password(password) and self.user_can_authenticate(user) :
            try:
                user = User.objects.using(db_name).get(username=username)
                return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None