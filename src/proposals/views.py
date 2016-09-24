from django.views.generic import CreateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
import logging

from .models import LogoProposal
from .forms import LogoProposalCreateForm


logger = logging.getLogger(__name__)


class LogoProposalCreateView(LoginRequiredMixin, CreateView):

    model = LogoProposal
    form_class = LogoProposalCreateForm
    success_url = reverse_lazy('index')
    template_name = 'proposals/new.html'

    def get_form_kwargs(self):
        """Pass request object for form creation"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Check if the number of proposals current user has is over the limit
        owner = self.request.user
        if owner.proposals.count() >= settings.NUM_PROPOSALS_PER_USER:
            messages.error(
                self.request,
                "You have exceeded the limit of max proposals one can submit. "
                "The latest submission is ineffective and ignored."
            )
            logger.error(
                "User %s exceeds the proposal submission limit." % owner.email
            )
            return redirect("index")
        else:
            return super().form_valid(form)
