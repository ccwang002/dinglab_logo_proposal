from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.views.generic import UpdateView, ListView

from .models import Review
from .forms import ReviewUpdateForm


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
                self.request.user.reviews
                .get(pk=self.kwargs['proposal_pk'])
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
