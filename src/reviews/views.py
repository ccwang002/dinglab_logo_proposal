from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import UpdateView, ListView
from django.views.decorators.http import require_POST
import itertools
import random

from proposals.models import LogoProposal
from .models import Review
from .forms import ReviewUpdateForm


@require_POST
@login_required
def create_new_review(request):
    reviewer = request.user

    if len(reviewer.reviews.all()) >= settings.NUM_REVIEWS_PER_USER:
        messages.error(
            request,
            "You have exceeded the maximum number of reviews."
        )
        return redirect('list_review')

    reviewed_proposals = {review.proposal_id for review in reviewer.reviews.all()}
    unseen_proposals = (
        LogoProposal.objects
        .exclude(id__in=reviewed_proposals)
        .exclude(owner_id=reviewer)
        .prefetch_related('reviews')
    )
    unseen_proposals_count = [
        p.reviews.count() for p in unseen_proposals
    ]
    weighted_unseen_proposals = list(itertools.chain.from_iterable([
        itertools.repeat(p, 3 - count)
        for p, count in zip(unseen_proposals, unseen_proposals_count)
        if count < 3
    ]))
    if not unseen_proposals:
        messages.warning(
            request,
            'All available proposals have been reviewed.'
        )
        return redirect('list_review')

    proposal_to_review = None
    if weighted_unseen_proposals:
        # means there are proposals to draw
        proposal_to_review = random.choice(weighted_unseen_proposals)
    else:
        # all proposals are sufficiently reviewed
        proposal_to_review = random.choice(unseen_proposals)

    Review.objects.create(
        reviewer=reviewer,
        proposal=proposal_to_review,
    )
    messages.info(
        request,
        'Create a new review for proposal #%d' % proposal_to_review.pk
    )
    return redirect('list_review')


class ReviewListView(LoginRequiredMixin, ListView):

    model = Review
    template_name = 'reviews/list.html'

    def get_queryset(self):
        reviewer = self.request.user
        return reviewer.reviews.all()


class ReviewEditView(LoginRequiredMixin, UpdateView):

    model = Review
    form_class = ReviewUpdateForm
    template_name = 'reviews/edit.html'
    success_url = reverse_lazy('list_review')

    def get_proposal(self):
        try:
            proposal = (
                Review.objects
                .filter(reviewer=self.request.user)
                .get(proposal=self.kwargs['proposal_pk'])
                .proposal
            )
        except self.model.DoesNotExist:
            raise Http404
        return proposal

    def get(self, request, *args, **kwargs):
        self.proposal = self.get_proposal()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.proposal = self.get_proposal()
        return super().post(request, *args, **kwargs)

    def get_object(self):
        try:
            review = Review.objects.get(
                reviewer=self.request.user,
                proposal=self.proposal,
            )
        except Review.DoesNotExist:
            review = None
        return review

    def get_form_kwargs(self):
        kwargs = {
            **super().get_form_kwargs(),
            'request': self.request,
            'proposal': self.proposal,
        }
        return kwargs


class ReviewStatView(LoginRequiredMixin, ListView):
    model = LogoProposal
    template_name = 'reviews/stat.html'

    def get(self, request, *args, **kwargs):
        after_review_deadline = (
            now() > settings.DATE_DISPLAY_REVIEW_STAT
        )
        if request.user.is_staff or after_review_deadline:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        ordered_proposals = self.model.objects.raw(
            'SELECT proposal_id AS id, avg(overall_impact) AS avg_score '
            'FROM reviews_review '
            'WHERE overall_impact NOT NULL '
            'GROUP BY proposal_id '
            'ORDER BY avg_score ASC '
        )
        return ordered_proposals
