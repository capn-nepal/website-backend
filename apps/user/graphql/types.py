import strawberry
import strawberry_django

from apps.user.models import User


@strawberry_django.type(User)
class UserType:
    id: strawberry.ID
    first_name: strawberry.auto
    last_name: strawberry.auto
    display_name: strawberry.auto


@strawberry_django.type(User)
class UserMeType:
    id: strawberry.ID
    email: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    display_name: strawberry.auto
