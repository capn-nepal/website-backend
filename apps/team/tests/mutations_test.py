import typing
from pathlib import Path

from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from apps.team.factories import TeamMemberFactory
from apps.team.models import TeamMemberTypeEnum
from apps.user.factories import UserFactory
from main import settings
from main.tests import TestCase

BASE_DIR = Path(__file__).resolve().parent


def team_member_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    member_data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100))
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": member_data},
            files={"memberPhoto": image_file},
            map={"memberPhoto": ["variables.data.memberPhoto"]},
            **kwargs,
        )


class TestTeamMemberMutation(TestCase):
    class Mutation:
        ADD_TEAM_MEMBER = """
          mutation AddTeamMember($data: CreateTeamMemberInput!) {
            addTeamMember(data: $data) {
              ... on TeamMemberTypeMutationResponseType {
                errors
                result {
                  id
                  firstName
                  middleName
                  lastName
                  designation
                  memberType
                  memberPhoto {
                    url
                  }
                }
              }
              ... on OperationInfo {
                __typename
                messages {
                  message
                }
              }
            }
          }
        """

        UPDATE_TEAM_MEMBER = """
          mutation UpdateTeamMember($pk: ID!, $data: UpdateTeamMemberInput!) {
            updateTeamMember(pk: $pk, data: $data) {
              ... on TeamMemberTypeMutationResponseType {
                errors
                result {
                  id
                  firstName
                  middleName
                  lastName
                  designation
                  memberType
                }
              }
              ... on OperationInfo {
                __typename
                messages {
                  message
                }
              }
            }
          }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="teamuser@example.com")

    def _create_member_mutation(self, member_data: dict, **kwargs):
        return team_member_query(
            query_check_func=self.query_check,
            query=self.Mutation.ADD_TEAM_MEMBER,
            member_data=member_data,
        )

    def _update_member_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_TEAM_MEMBER,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def test_add_team_member(self):
        member_data = {
            "firstName": "Alice",
            "middleName": "B.",
            "lastName": "Smith",
            "designation": "CEO",
            "memberType": TeamMemberTypeEnum.BOARD_MEMBER.name,
        }

        # Without authentication
        content = self._create_member_mutation(member_data)
        assert content["data"]["addTeamMember"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_member_mutation(member_data)
        resp = content["data"]["addTeamMember"]
        assert resp["errors"] is None
        assert {
            "firstName": resp["result"]["firstName"],
            "middleName": resp["result"]["middleName"],
            "lastName": resp["result"]["lastName"],
            "designation": resp["result"]["designation"],
            "memberType": resp["result"]["memberType"],
        } == {
            "firstName": member_data["firstName"],
            "middleName": member_data["middleName"],
            "lastName": member_data["lastName"],
            "designation": member_data["designation"],
            "memberType": member_data["memberType"],
        }
        assert "url" in resp["result"]["memberPhoto"]

    def test_update_team_member(self):
        member = TeamMemberFactory.create(
            first_name="Old",
            middle_name="X",
            last_name="Name",
            designation="Manager",
            member_type=TeamMemberTypeEnum.TEAM_MEMBER,
        )
        update_data = {
            "firstName": "New",
            "middleName": "Y",
            "lastName": "Updated",
            "designation": "CTO",
        }

        # Without authentication
        content = self._update_member_mutation(self.gID(member.pk), update_data)
        assert content["data"]["updateTeamMember"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._update_member_mutation(self.gID(member.pk), update_data)
        resp = content["data"]["updateTeamMember"]
        assert resp["errors"] is None
        assert {
            "firstName": resp["result"]["firstName"],
            "middleName": resp["result"]["middleName"],
            "lastName": resp["result"]["lastName"],
            "designation": resp["result"]["designation"],
        } == {
            "firstName": update_data["firstName"],
            "middleName": update_data["middleName"],
            "lastName": update_data["lastName"],
            "designation": update_data["designation"],
        }
