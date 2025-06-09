from apps.user.factories import UserFactory
from apps.vacancy.factories import JobVacancyFactory, PositionFactory
from apps.vacancy.models import EmployMentTypeEnum
from main.tests.base_test import TestCase


class TestJobVacancyQuery(TestCase):
    class Query:
        JOB_VACANCIES = """
            query jobVacancies($pagination: OffsetPaginationInput, $order: JobVacancyOrder) {
                jobVacancies(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        description
                        deadline
                        numberOfVacancies
                        position {
                            pk
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="vacancyuser@example.com")
        cls.position = PositionFactory.create(
            name="name1",
            employment_type=EmployMentTypeEnum.TEMPORARY,
            summary="summary1",
            key_responsibilities="somthing",
            qualifications="q",
            preferred_skills="skills",
        )

        cls.vacancies = [
            JobVacancyFactory.create(
                description="Vacancy 1",
                deadline="2025-12-01",
                number_of_vacancies=2,
                position=cls.position,
            ),
            JobVacancyFactory.create(
                description="Vacancy 2",
                deadline="2025-12-05",
                number_of_vacancies=3,
                position=cls.position,
            ),
        ]

    def test_job_vacancies_query(self):
        def _query():
            return self.query_check(
                self.Query.JOB_VACANCIES,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without authentication
        content = _query()
        assert content["data"]["jobVacancies"]["totalCount"] == 0
        #  With authentication
        self.force_login(self.user)
        content = _query()
        assert content["data"]["jobVacancies"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(vacancy.pk),
                        description=vacancy.description,
                        deadline=str(vacancy.deadline),
                        numberOfVacancies=vacancy.number_of_vacancies,
                        position={"pk": self.gID(vacancy.position.pk)},
                    )
                    for vacancy in self.vacancies
                ],
            ),
        }, content


class TestPositionQuery(TestCase):
    class Query:
        POSITIONS = """
            query positions($pagination: OffsetPaginationInput, $order: PositionOrder) {
                positions(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        name
                        summary
                        keyResponsibilities
                        qualifications
                        preferredSkills
                        employmentType
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="posuser@example.com")
        cls.positions = [
            PositionFactory.create(
                name="Position A",
                employment_type=EmployMentTypeEnum.FULL_TIME,
                summary="Summary A",
                key_responsibilities="Responsibilities A",
                qualifications="Qualifications A",
                preferred_skills="Skills A",
            ),
            PositionFactory.create(
                name="Position B",
                employment_type=EmployMentTypeEnum.CONTRACT,
                summary="Summary B",
                key_responsibilities="Responsibilities B",
                qualifications="Qualifications B",
                preferred_skills="Skills B",
            ),
        ]

    def test_positions_query(self):
        def _query():
            return self.query_check(
                self.Query.POSITIONS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without authentication
        content = _query()
        assert content["data"]["positions"]["totalCount"] == 0

        # With authentication
        self.force_login(self.user)
        content = _query()
        assert content["data"]["positions"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(position.pk),
                        name=position.name,
                        summary=position.summary,
                        keyResponsibilities=position.key_responsibilities,
                        qualifications=position.qualifications,
                        preferredSkills=position.preferred_skills,
                        employmentType=position.employment_type.name,
                    )
                    for position in self.positions
                ],
            ),
        }, content
