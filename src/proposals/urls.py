from django.conf.urls import url

from .views import LogoProposalCreateView

urlpatterns = [
    url(r'^new/$', LogoProposalCreateView.as_view(), name='new_proposal'),
]
