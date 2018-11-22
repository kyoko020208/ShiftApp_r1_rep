from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AuthUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, phone, password):
        """
        Create users
        :param first_name: First name
        :param last_name: Last name
        :param phone: Mobile phone number
        :param password: Password
        :return: AuthUser object
        """

        if not username:
            raise ValueError('username is required')

        if not first_name:
            raise ValueError('First Name is required')

        if not last_name:
            raise ValueError('Last Name is required')

        if not password:
            raise ValueError('Password is required')

        if not phone:
            raise ValueError('Phone is required')


        user = self.model(username=username,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          password=password)

        user.is_active =True
        user.ser_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, phone, password, restaurants):
        """
        create super user
        """
        user = self.create_user(first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class AuthUser(AbstractBaseUser, PermissionsMixin):
    """
    Manage User Info
    """
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def get_full_name(self):
        """
        Get user's full name
        :return: first_name + last_name
        """
        return self.last_name + self.first_name

    username = models.CharField(verbose_name='username', max_length=30, unique=True)

    first_name = models.CharField(verbose_name='first name', max_length=30)

    last_name = models.CharField(verbose_name='last name', max_length=30)

    phone = models.CharField(verbose_name='Phone Number', max_length=15)

    password = models.CharField(verbose_name='password', max_length=128)

    restaurant = models.CharField(verbose_name='restaurants', max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)

    #Check if he already exists in the list
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
    )


    #Check if he is a manager
    is_manager = models.BooleanField(
        verbose_name='manager status',
        default=False,
    )

    # Check if the account is active
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = AuthUserManager()

    def __str__(self):
        return self.last_name + ' ' + self.first_name