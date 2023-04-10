from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for User model with no username field."""
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError('Enter a functional email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

