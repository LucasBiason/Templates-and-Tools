from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """ Create and saves the new user """
        if not username:
            raise ValueError(_("User must have username address"))
        user = self.model(
            username=username, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        """ Create and saves the new superuser """
        user = self.create_user(username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user models that suppors using username instead of username """
    
    username = models.CharField(
        _('Username'), 
        max_length=50, 
        unique=True, blank=False
    )

    is_active = models.BooleanField(
        _('Active'), default=True
    )

    is_staff = models.BooleanField(
       _('Staff'), default=False
    )

    is_superuser = models.BooleanField(
        _('Super User'), default=False
    )

    first_name = models.CharField(
        _('First Name'), 
        max_length=30, 
        default=''
    )

    last_name = models.CharField(
        _('Last Name'), 
        max_length=30, 
        default=''
    )
    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'