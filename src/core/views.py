from itertools import zip_longest
from django.views.generic.base import TemplateView
from proposals.models import LogoProposal


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposals = LogoProposal.objects.all()
        proposals_list = list(grouper(proposals, 3))
        proposals_list[-1] = [p for p in proposals_list[-1] if p]
        context['proposals_list'] = proposals_list
        return context
