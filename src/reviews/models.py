from django.conf import settings
from django.core.validators import (
    MaxValueValidator, MinValueValidator, int_list_validator
)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class IntegerRangeField(models.IntegerField):

    def __init__(self, *args, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value

        validators = kwargs.get('validators', [])
        if isinstance(max_value, int):
            validators.append(MaxValueValidator(max_value))
        if isinstance(min_value, int):
            validators.append(MinValueValidator(min_value))
        kwargs['validators'] = validators

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.min_value,
            'max_value': self.max_value,
            **kwargs,
        }
        return super().formfield(**defaults)


class ReviewScoreField(IntegerRangeField):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            "min_value": 1,
            "max_value": 9,
            "null": True, "blank": True,
        })
        super().__init__(*args, **kwargs)


class Review(models.Model):

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    proposal = models.ForeignKey(
        "proposals.LogoProposal",
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    significance = ReviewScoreField(
        help_text=_(
            "Symbolize key characteristics of the lab. "
            "Inspiration. Simple but meaningful."
        ),
    )

    innovation = ReviewScoreField(
        help_text=_(
            "Original but not at the expense of the message. "
            "Unique but not odd. Creative but not ugly."
        ),
    )

    approach = ReviewScoreField(
        help_text=_(
            "The use of color, shape, pattern, and pictures. "
            "Is it captivating and easy on your eyes?"
        ),
    )

    investigator = ReviewScoreField(
        help_text=_(
            "NIH evaluates investigators to gauge the chance of getting "
            "the proposed products. We are evaluating the finished products. "
            "So, what is the point?!"
        ),
    )

    environment = ReviewScoreField(
        default=1,
        help_text=_("Nothing. Give 1 to everyone."),
    )

    overall_impact = ReviewScoreField()

    comment = models.TextField(null=True, blank=True)

    comment_disclosure = models.BooleanField(
        default=True,
        help_text=_(
            "Whether the comment is disclosed to the submitter."
        ),
    )

    class Meta:
        unique_together = (("reviewer", "proposal"),)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('edit_review', kwargs={'proposal_pk': self.proposal.pk})

    def __str__(self):
        return 'Proposal #{:d} by {:s}'.format(
            self.proposal_id, self.reviewer.get_repr_name()
        )


class StudySectionReview(models.Model):

    proposal = models.ForeignKey(
        "proposals.LogoProposal",
        on_delete=models.CASCADE,
        related_name='study_reviews',
    )

    raw_score_list = models.CharField(
        validators=[int_list_validator(), ],
        max_length=512,
    )

    summary = models.TextField(blank=True, default='')

    def __str__(self):
        return 'Study section score of proposal #{:d}'.format(
            self.proposal_id
        )

# for p_id, scores in scores_by_proposals.items():
#     proposal = LogoProposal.objects.get(pk=p_id)
#     ss_review = StudySectionReview(
#          proposal=proposal,
#          raw_score_list=','.join(map(str, scores))
#     )
#     print(ss_review)
#     ss_review.save()
