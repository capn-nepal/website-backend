from django.contrib import admin

from apps.team.models import TeamMember


@admin.register(TeamMember)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "designation", "member_type", "member_order")
    list_filter = ("member_type", "designation")
    ordering = ("member_order",)
