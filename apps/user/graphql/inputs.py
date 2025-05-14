import strawberry
import strawberry_django

from apps.user.models import User


@strawberry_django.input(User)
class LoginInput:
    email: strawberry.auto
    password: strawberry.auto
