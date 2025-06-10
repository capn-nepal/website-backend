from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import UserResource


class EmploymentTypeEnum(models.IntegerChoices):
    FULL_TIME = 10, "Full Time"
    PART_TIME = 20, "Part Time"
    CONTRACT = 30, "Contract"
    INTERNSHIP = 40, "Internship"
    TEMPORARY = 50, "Temporary"


class Position(UserResource):
    name = models.CharField(max_length=255, verbose_name=_("Position Name"))
    summary = models.TextField(verbose_name=_("Position Summary"))
    description = models.TextField(verbose_name=_("Description"))
    employment_type: int = IntegerChoicesField(choices_enum=EmploymentTypeEnum)  # type: ignore[reportAssignmentType]
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class JobVacancy(UserResource):
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="position")
    description = models.TextField(verbose_name=_("Vacancy Description"))
    number_of_vacancies = models.PositiveIntegerField()
    deadline = models.DateField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.position.name} - {self.id}"
