from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Layout, Submit
from crispy_forms.bootstrap import FormActions
from django import forms
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.forms import RequestUserValidationMixin
from .models import LogoProposal


class LogoProposalCreateForm(RequestUserValidationMixin, forms.ModelForm):

    class Meta:
        model = LogoProposal
        fields = ('logo', 'description',)

    def save(self, commit=True):
        """Fill owner field on save."""
        proposal = super().save(commit=False)
        proposal.owner = self._request.user
        if commit:
            proposal.save()
        return proposal

    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            Fieldset(
                '',
                Field('logo'),
                Field('description'),
            ),
            FormActions(
                Submit(
                    'save', _('Create Account'), css_class='btn-lg btn-block',
                )
            )
        )
        return helper
