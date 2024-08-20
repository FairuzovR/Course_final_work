from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from .utils import normalize_phone_number
import logging
logger = logging.getLogger('user')


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Необходим номер телефона')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser):
    phone_number = models.CharField(
            max_length=15, unique=True,
            validators=[RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'. \
Разрешено от 9 до 15 ."
            )]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.phone_number = normalize_phone_number(self.phone_number)
        logger.debug(f'Normilized number: {self.phone_number}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number
