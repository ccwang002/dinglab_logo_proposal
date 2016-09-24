from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView
import logging

from .models import LogoProposal
from .forms import LogoProposalCreateForm


logger = logging.getLogger(__name__)


class LogoProposalCreateView(LoginRequiredMixin, CreateView):

    model = LogoProposal
    form_class = LogoProposalCreateForm
    success_url = reverse_lazy('list_proposal')
    template_name = 'proposals/new.html'

    def over_proposal_limit(self):
        owner = self.request.user
        if owner.proposals.count() >= settings.NUM_PROPOSALS_PER_USER:
            messages.error(
                self.request,
                "You have reached the limit of max proposals one can submit. "
            )
            logger.error(
                "User %s exceeds the proposal submission limit." % owner.email
            )
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if self.over_proposal_limit():
            return redirect("index")
        else:
            return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass request object for form creation"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Check if the number of proposals current user has is over the limit
        if self.over_proposal_limit():
            messages.error(
                self.request,
                "The latest proposal submission is ineffective and ignored."
            )
            return redirect("index")
        else:
            return super().form_valid(form)


class LogoProposalListView(LoginRequiredMixin, ListView):

    model = LogoProposal
    template_name = 'proposals/list.html'

    def get_queryset(self):
        owner = self.request.user
        return owner.proposals.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_proposals = self.request.user.proposals.count()
        context.update({
            'has_quota': num_proposals < settings.NUM_PROPOSALS_PER_USER
        })
        return context


class LogoProposalUpdateView(LoginRequiredMixin, UpdateView):

    model = LogoProposal
    form_class = LogoProposalCreateForm
    template_name = 'proposals/edit.html'
    success_url = reverse_lazy('list_proposal')

    def get_form_kwargs(self):
        """Pass request object for form creation"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
