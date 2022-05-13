from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _

from src.utils import validators


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """ Create and saves the new user """
        if not username:
            raise ValueError(_("User must have username"))
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
    
    @classmethod
    def retrieve(cls, user_pk, **kwargs):
        try:
            if str(user_pk).isdigit():
                users = cls.objects.filter(pk=user_pk)
            else:
                users = cls.objects.filter(username=user_pk)
            if kwargs.get('exclude'):
                users = users.exclude(pk=kwargs['exclude'])
            return users.get()
        except Exception as e:
            if 'silence' in kwargs:
                return None
            raise Exception( 'USER NOT FOUND')  
    
    @classmethod
    def get_queryset(cls, **kwargs):      
        queryset = cls.objects.all()
        return queryset

    @classmethod
    def perform_create(cls, data, user_creator):
        cls.validate_can_manage(user_creator)
        data['is_active'] = True
        user = cls._set_data_and_save(data)
        return user

    def perform_update(self, data, user_creator):
        self.validate_can_manage(user_creator)
        data['id'] = self.id
        data['is_active'] = True
        user = self._set_data_and_save(data, user=self)
        return self

    @classmethod
    def validate_can_manage(cls, user_creator):
        if not user_creator.is_superuser:
            raise Exception('This logged user does not have permissions to manager users')
        return True
    
    @classmethod
    def validate_username(cls, username, exclude=None):       
        if cls.retrieve(username, exclude=exclude, silence=True)  :
            raise Exception('USER ALREADY CREATED')
        return username

    @classmethod
    def validate_first_name(cls, first_name):
        valid, first_name = validators.validate_text(
            first_name,  max_length=30, required=True
        )
        if not valid:
            raise Exceptionr('FIRST NAME INVALID')
        return first_name

    @classmethod
    def validate_last_name(cls, last_name):
        valid, last_name = validators.validate_text(
            last_name, max_length=30, required=True
        )
        if not valid:
            raise Exceptionr('LAST NAME INVALID')
        return last_name

    @classmethod
    def _set_data_and_save(cls, data, user=None):
        username = cls.validate_username(
            data.get('username'), 
            exclude=user.id if user else None
        )
        
        if not user:
            user = cls.retrieve(username, silence=True)
            if not user:
                user = cls()
                user.username = username
        
        user.first_name = cls.validate_first_name(data.get('first_name'))
        user.last_name = cls.validate_last_name(data.get('last_name'))
        
        if data.get('password'):
            user.set_password(data.get('password'))
                
        user.save()
        return user