from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, HTML, Div, Layout, Submit
from crispy_forms.bootstrap import FormActions
from django import forms
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.forms import RequestUserValidationMixin
from .models import Review


class ReviewUpdateForm(RequestUserValidationMixin, forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('reviewer', 'proposal', )

    def __init__(self, proposal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proposal = proposal

        # Make sure user submit the overall impact score
        for score_field in [
            # 'significance', 'innovation',
            # 'approach', 'investigator', 'environment',
            'overall_impact'
        ]:
            self.fields[score_field].required = True

    def save(self, commit=True):
        review = super().save(commit=False)
        review.reviewer = self._request.user
        review.proposal = self._proposal
        if commit:
            review.save()
        return review

    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-8'
        helper.layout = Layout(
            Fieldset(
                'Criteria',
                'significance',
                'innovation',
                'approach',
                'investigator',
                'environment',
                'overall_impact',
                HTML("""
                <p>
                Scores: 1-3 from unbelievable to excellent;
                4-6 from good to so so;
                7-9 from "will not be discussed" to "will not be discussed. <br>
                Ref: <a href="https://grants.nih.gov/grants/peer/guidelines_general/scoring_system_and_procedure.pdf" target="_blank">
                    NIH scoring system and procedure</a>
                </p>
                """),
            ),
            Fieldset(
                'Comment',
                'comment',
                'comment_disclosure',
            ),
            FormActions(
                Submit(
                    'save', _('Submit'), css_class='btn-lg btn-block',
                )
            )
        )
        return helper
