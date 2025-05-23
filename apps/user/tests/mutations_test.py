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
        CHANGE_PASSWORD_MUTATION = """
            mutation ChangePassword($data: ChangePasswordInput!) {
              changePassword(data: $data) {
                ... on OperationInfo {
                  __typename
                  messages {
                    message
                  }
                }
                ... on UserMeTypeMutationResponseType {
                  ok
                  errors
                }
              }
            }
        """

    def setUp(self):
        super().setUp()
        self.user1 = UserFactory.create(email="testuser1@gmail.com", is_active=True)

        self.password = "OldPass123!"
        self.user2 = UserFactory.create(email="changepass@example.com", is_active=True)
        self.user2.set_password(self.password)
        self.user2.save()

    def _query_login(self, data: dict, **kwargs):
        return self.query_check(self.Mutation.LOGIN_MUTATION, variables={"data": data}, **kwargs)

    def _change_password(self, data: dict, **kwargs):
        return self.query_check(self.Mutation.CHANGE_PASSWORD_MUTATION, variables={"data": data}, **kwargs)

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

    def test_change_password(self):
        self.force_login(self.user2)

        # with wrong old password
        response = self._change_password(
            {
                "oldPassword": "WrongPass@@",
                "newPassword": "New@@@Pass123!",
            },
        )
        result = response["data"]["changePassword"]
        assert result["ok"] is False
        assert result["errors"] is not None

        #  with correct old password
        response = self._change_password(
            {
                "oldPassword": self.password,
                "newPassword": "New@@@Pass123!",
            },
        )
        result = response["data"]["changePassword"]
        assert result["errors"] is None

        # login with new password
        self.client.logout()
        login_response = self._query_login({"email": self.user2.email, "password": "New@@@Pass123!"})
        login_result = login_response["data"]["login"]
        assert login_result["ok"] is True
        assert login_result["result"]["email"] == self.user2.email
