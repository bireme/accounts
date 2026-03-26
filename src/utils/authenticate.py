from django.contrib.auth.models import User


class EmailModelBackend:
    """
    Authentication backend that allows users to log in using their email address
    instead of username.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Authenticate a user using their email address.

        Args:
            request: The request object
            username: The email address (used as username)
            password: The user's password

        Returns:
            User object if authentication is successful, None otherwise
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Get a user by their ID.

        Args:
            user_id: The user's primary key

        Returns:
            User object if found, None otherwise
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None