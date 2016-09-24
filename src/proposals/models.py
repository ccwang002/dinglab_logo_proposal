from pathlib import Path

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


def gen_logo_filename(proposal, filename):
    return str(Path(
        'logos/{email}_{filename}'
        .format(
            email=proposal.owner.email.replace('@', '_AT_'),
            filename=filename
        )
    ))


class LogoProposal(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proposals',
    )

    logo = models.ImageField(
        upload_to=gen_logo_filename,
    )

    description = models.TextField(
        max_length=420,
        blank=True,
        help_text=_(
            'Description of the logo proposal. Can be the philosophy or story '
            'behind the design. Should be fit within three Tweets '
            '(less than 420 chars).'
        )
    )
