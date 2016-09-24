from django.contrib import admin

from .models import LogoProposal


@admin.register(LogoProposal)
class LogoProposalAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'owner',
        'logo',
    )
