from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import UserResource
from utils.fields import SecureImageField


class TeamMemberTypeEnum(models.IntegerChoices):
    BOARD_MEMBER = 80, "Board Member"
    TEAM_MEMBER = 90, "Team Member"


class TeamMember(UserResource):
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Middle Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    bio = models.TextField(verbose_name=_("Bio"), null=True, blank=True)
    designation = models.CharField(max_length=150, verbose_name=_("Designation"))
    member_photo = SecureImageField(upload_to="member_photos/", blank=True, null=True)
    member_type: int = IntegerChoicesField(choices_enum=TeamMemberTypeEnum, default=TeamMemberTypeEnum.TEAM_MEMBER)  # type: ignore[reportAssignmentType]

    def __str__(self):
        return self.first_name
