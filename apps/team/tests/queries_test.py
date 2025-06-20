from apps.team.factories import TeamMemberFactory
from apps.team.models import TeamMemberTypeEnum
from apps.user.factories import UserFactory
from main.tests import TestCase


class TestTeamMemberQuery(TestCase):
    class Query:
        TEAM_MEMBERS = """
          query teamMembers($pagination: OffsetPaginationInput, $order: TeamMemberOrder) {
            teamMembers(pagination: $pagination, order: $order) {
              totalCount
              results {
                id
                firstName
                middleName
                lastName
                designation
                memberPhoto {
                  url
                }
              }
              pageInfo {
                limit
                offset
              }
            }
          }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="team@example.com")

    def test_team_members_query(self):
        def _query():
            return self.query_check(
                self.Query.TEAM_MEMBERS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        members = [
            TeamMemberFactory.create(
                first_name="Alice",
                middle_name="B.",
                last_name="Smith",
                designation="Lead Engineer",
                member_type=TeamMemberTypeEnum.BOARD_MEMBER,
            ),
            TeamMemberFactory.create(
                first_name="Bob",
                middle_name="C.",
                last_name="Jones",
                designation="Product Manager",
                member_type=TeamMemberTypeEnum.BOARD_MEMBER,
            ),
        ]

        content = _query()
        assert content["data"]["teamMembers"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(member.id),
                        firstName=member.first_name,
                        middleName=member.middle_name,
                        lastName=member.last_name,
                        designation=member.designation,
                        memberPhoto={"url": member.member_photo.url} if member.member_photo else None,
                    )
                    for member in members
                ],
            ),
        }, content
