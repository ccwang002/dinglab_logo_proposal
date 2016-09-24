from django.conf.urls import url

from .views import (
    LogoProposalCreateView,
    LogoProposalListView,
    LogoProposalUpdateView,
)

urlpatterns = [
    url(r'^new/$', LogoProposalCreateView.as_view(), name='new_proposal'),
    url(r'^list/$', LogoProposalListView.as_view(), name='list_proposal'),
    url(r'^edit/(?P<pk>\d+)/$', LogoProposalUpdateView.as_view(), name='edit_proposal'),
]
