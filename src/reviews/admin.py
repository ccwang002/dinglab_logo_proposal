from django.contrib import admin

from .models import Review, StudySectionReview


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'reviewer',
        'proposal',
        'overall_impact',
    )


@admin.register(StudySectionReview)
class StudySectionReviewAdmin(admin.ModelAdmin):

    list_display = (
        'proposal',
        'raw_score_list',
    )
