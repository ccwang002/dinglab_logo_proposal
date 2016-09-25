from django.conf.urls import url

from .views import (
    ReviewListView,
    ReviewEditView,
    create_new_review,
)

urlpatterns = [
    url(r'^$', ReviewListView.as_view(), name='list_review'),
    url(r'^edit/(?P<proposal_pk>\d+)/$', ReviewEditView.as_view(), name='edit_review'),
    url(r'^new/$', create_new_review, name='new_review'),
]
