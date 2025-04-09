import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        error_messages={"unique": "そのユーザー名はすでに存在します。"},
        help_text="必須。30文字以下。文字、数字、@ / . / + / - / _ のみ。",
        max_length=30,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name="username",
    )
    password = models.CharField(max_length=128, verbose_name="password")
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    whisky = models.ForeignKey(
        "notes.Whisky",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_whisky",
    )

    def __str__(self):
        return str(self.username)
