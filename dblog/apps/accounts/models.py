from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)