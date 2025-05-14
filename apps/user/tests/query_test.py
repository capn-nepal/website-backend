from apps.user.factories import UserFactory
from main.tests import TestCase


class TestUserQuery(TestCase):
    class Query:
        ME = """
            query meQuery {
              me {
                id
                email
                firstName
                lastName
                displayName
              }
            }
        """
        USERS = """
            query users($pagination: OffsetPaginationInput) {
            users(pagination: $pagination) {
                totalCount
                pageInfo {
                offset
                limit
                }
                results {
                    id
                    email
                    firstName
                    lastName
                    displayName
                }
            }
        }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = UserFactory.create(email="hero@gmail.com")
        # Some other users as well
        cls.users = [
            UserFactory.create(first_name="Test", last_name="Hero", email="sample@test.com"),
            UserFactory.create(first_name="Example", last_name="Villain", email="sample@vil.com"),
            UserFactory.create(first_name="Test", last_name="Hero"),
        ]

    def test_me(self):
        # Without authentication -----
        content = self.query_check(self.Query.ME)
        assert content["data"]["me"] is None

        user = self.user1
        # With authentication -----
        self.force_login(user)
        content = self.query_check(self.Query.ME)
        assert content["data"]["me"] == dict(
            id=self.gID(user.id),
            email=user.email,
            firstName=user.first_name,
            lastName=user.last_name,
            displayName=f"{user.first_name} {user.last_name}",
        )

    def test_users_query(self):
        def _query():
            return self.query_check(
                self.Query.USERS,
                variables={
                    "pagination": {
                        "limit": 10,
                        "offset": 0,
                    },
                },
            )

        # Without authentication
        content = _query()
        assert content["data"]["users"]["totalCount"] == 0

        # Create a new active user and login
        user = UserFactory.create(email="hero2@gmail.com", is_active=True)
        self.force_login(user)
        content = _query()

        expected_users = [self.user1] + self.users + [user]

        assert content["data"]["users"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=5,
                results=[
                    dict(
                        id=self.gID(u.id),
                        email=u.email,
                        firstName=u.first_name,
                        lastName=u.last_name,
                        displayName=f"{u.first_name} {u.last_name}",
                    )
                    for u in expected_users
                ],
            ),
        }, content
