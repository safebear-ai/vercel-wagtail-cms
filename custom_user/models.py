from django.db import models
# Create your models here.
from wagtail.users.models import UserProfile
import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uuid.uuid4(), filename=filename, ext=ext
        ),
    )

class CustomUserProfile(UserProfile):
    custom_avatar = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to=upload_avatar_to,
        blank=True,
        max_length=255,
    )
