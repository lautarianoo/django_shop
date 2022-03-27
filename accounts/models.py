import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):

    email = models.EmailField("Email" ,blank=True, unique=True)
    first_name = models.CharField("Имя",blank=True, max_length=30)
    last_name = models.CharField("Фамилия", blank=True, max_length=30)
    phone = models.CharField("Телефон", blank=True, null=True, max_length=16)
    avatar = models.ImageField("Аватар", blank=True)
    status_email = models.BooleanField("Подтверждён Email", default=False)
    date_reg = models.DateTimeField("Дата регистрации", auto_now_add=True)
    is_admin = models.BooleanField("Админ", default=False)
    banned = models.BooleanField("Забанен", default=False)

    object = MyUserManager()

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if self.avatar:
            image = self.avatar
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.avatar.name.split('.'))
            self.avatar = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_admin

