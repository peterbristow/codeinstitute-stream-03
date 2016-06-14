from models import User


class EmailAuth(object):
    def authenticate(self, email=None, password=None):
        """
        Override the authenticate method.
        Test against email instead if the username.
        Get an instance of User, using the supplied
        email and check its password.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user() method.
        Applies an extra condition to the login process.
        Used by django authentication system to retrieve an
        instance of the user.
        Make sure user is active and whether they can login.
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
