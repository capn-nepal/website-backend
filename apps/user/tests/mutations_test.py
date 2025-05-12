from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestUserMutation(TestCase):
    class Mutation:
        LOGIN_MUTATION = """
            mutation Login($data: LoginInput!) {
                login(data: $data) {
                    ok
                    errors
                    result {
                        id
                        email
                        displayName
                    }
                }
            }
        """

    def setUp(self):
        super().setUp()
        self.user1 = UserFactory.create(email="testuser1@gmail.com", is_active=True)

    def _query_login(self, data: dict, **kwargs):
        return self.query_check(self.Mutation.LOGIN_MUTATION, variables={"data": data}, **kwargs)

    def test_login(self):
        password = "StrongPass123!"
        user = UserFactory.create(email="login@example.com", password=password, is_active=True)
        # NOTE: Django's create_user hash passwords, but factory may not. Set manually.
        user.set_password(password)
        user.save()
        # logging in with wrong credentials
        response = self._query_login({"email": user.email, "password": "WrongPass!"})
        result = response["data"]["login"]
        assert result["ok"] is False
        assert result["errors"] is not None
        # logging in with correct credentials
        response = self._query_login({"email": user.email, "password": password})
        result = response["data"]["login"]
        assert result["ok"] is True
        assert result["errors"] is None
        assert result["result"]["email"] == user.email
