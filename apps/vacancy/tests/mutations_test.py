from apps.user.factories import UserFactory
from apps.vacancy.factories import JobVacancyFactory, PositionFactory
from apps.vacancy.models import EmployMentTypeEnum
from main.tests.base_test import TestCase


class TestJobVacancyMutation(TestCase):
    class Mutation:
        CREATE_VACANCY = """
            mutation CreateJobVacancy($data: CreateJobVacancyInput!) {
                createJobVacancy(data: $data) {
                    ... on JobVacancyTypeMutationResponseType {
                        errors
                        result {
                            id
                            description
                            deadline
                            numberOfVacancies
                            position {
                                pk
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

        UPDATE_VACANCY = """
            mutation UpdateJobVacancy($pk: ID!, $data: UpdateJobVacancyInput!) {
                updateJobVacancy(pk: $pk, data: $data) {
                    ... on JobVacancyTypeMutationResponseType {
                        ok
                        errors
                        result {
                            id
                            description
                            deadline
                            numberOfVacancies
                            position {
                                pk
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

        ARCHIVE_VACANCY = """
            mutation ArchiveJobVacancy($pk: ID!) {
                archiveJobVacancy(pk: $pk) {
                    ... on JobVacancyTypeMutationResponseType {
                        errors
                        result {
                            id
                            description
                            deadline
                            numberOfVacancies
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
        cls.user = UserFactory.create(email="vacancyuser@example.com")
        cls.position = PositionFactory.create(
            name="Test Position",
            employment_type=EmployMentTypeEnum.TEMPORARY,
            summary="Summary",
            key_responsibilities="Responsibilities",
            qualifications="Qualifications",
            preferred_skills="Skills",
        )

    def _create_vacancy_mutation(self, data: dict, **kwargs):
        return self.query_check(
            self.Mutation.CREATE_VACANCY,
            variables={"data": data},
        )

    def _update_vacancy_mutation(self, pk: str, data: dict, **kwargs):
        return self.query_check(
            self.Mutation.UPDATE_VACANCY,
            variables={"pk": pk, "data": data},
        )

    def _archive_vacancy_mutation(self, pk: str, **kwargs):
        return self.query_check(
            self.Mutation.ARCHIVE_VACANCY,
            variables={"pk": pk},
        )

    def test_create_job_vacancy(self):
        data = {
            "description": "New job vacancy",
            "deadline": "2025-12-01",
            "numberOfVacancies": 5,
            "position": self.position.pk,
        }
        # Without authentication
        content = self._create_vacancy_mutation(data)
        assert content["data"]["createJobVacancy"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._create_vacancy_mutation(data)
        response_data = content["data"]["createJobVacancy"]
        assert response_data["errors"] is None
        assert response_data["result"]["description"] == data["description"]
        assert response_data["result"]["deadline"] == data["deadline"]
        assert response_data["result"]["numberOfVacancies"] == data["numberOfVacancies"]

    def test_update_job_vacancy(self):
        vacancy = JobVacancyFactory.create(
            position=self.position,
            description="Old desc",
            deadline="2025-12-01",
            number_of_vacancies=2,
        )
        data = {
            "description": "Updated desc",
            "deadline": "2025-12-31",
            "numberOfVacancies": 10,
            "position": self.position.pk,
        }
        # Without authentication
        content = self._update_vacancy_mutation(str(vacancy.pk), data)
        assert content["data"]["updateJobVacancy"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._update_vacancy_mutation(str(vacancy.pk), data)
        response_data = content["data"]["updateJobVacancy"]
        assert response_data["errors"] is None, content
        vacancy.refresh_from_db()
        assert response_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(vacancy.pk),
                description=vacancy.description,
                deadline=str(vacancy.deadline),
                numberOfVacancies=vacancy.number_of_vacancies,
                position={"pk": self.gID(vacancy.position.pk)},
            ),
        ), content

    def test_archive_job_vacancy(self):
        vacancy = JobVacancyFactory.create(
            position=self.position,
            description="Archive this",
            deadline="2025-12-01",
            number_of_vacancies=3,
        )
        # Without authentication
        content = self._archive_vacancy_mutation(str(vacancy.pk))
        assert content["data"]["archiveJobVacancy"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._archive_vacancy_mutation(str(vacancy.pk))
        response_data = content["data"]["archiveJobVacancy"]
        assert response_data["errors"] is None, content
        vacancy.refresh_from_db()
        assert vacancy.is_archived is True


class TestPositionMutation(TestCase):
    class Mutation:
        CREATE_POSITION = """
            mutation CreatePosition($data: CreatePositionInput!) {
                createPosition(data: $data) {
                    ... on PositionTypeMutationResponseType {
                        errors
                        result {
                            id
                            name
                            summary
                            keyResponsibilities
                            qualifications
                            preferredSkills
                            employmentType
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

        UPDATE_POSITION = """
            mutation UpdatePosition($pk: ID!, $data: UpdatePositionInput!) {
                updatePosition(pk: $pk, data: $data) {
                    ... on PositionTypeMutationResponseType {
                        ok
                        errors
                        result {
                            id
                            name
                            summary
                            keyResponsibilities
                            qualifications
                            preferredSkills
                            employmentType
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

        ARCHIVE_POSITION = """
            mutation ArchivePosition($pk: ID!) {
                archivePosition(pk: $pk) {
                    ... on PositionTypeMutationResponseType {
                        errors
                        result {
                            id
                            name
                            summary
                            keyResponsibilities
                            qualifications
                            preferredSkills
                            employmentType
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
        cls.user = UserFactory.create(email="vacancyuser@example.com")

    def _create_position_mutation(self, data: dict):
        return self.query_check(
            self.Mutation.CREATE_POSITION,
            variables={"data": data},
        )

    def _update_position_mutation(self, pk: str, data: dict):
        return self.query_check(self.Mutation.UPDATE_POSITION, variables={"pk": pk, "data": data})

    def _archive_position_mutation(self, pk: str, **kwargs):
        return self.query_check(self.Mutation.ARCHIVE_POSITION, variables={"pk": pk})

    def test_create_position(self):
        data = {
            "name": "Position1",
            "employmentType": EmployMentTypeEnum.TEMPORARY.name,
            "summary": "Summary1",
            "keyResponsibilities": "Responsibilities",
            "qualifications": "Qualifications",
            "preferredSkills": "Skills",
        }

        # Without authentication
        content = self._create_position_mutation(data)
        assert content["data"]["createPosition"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_position_mutation(data)
        response_data = content["data"]["createPosition"]
        assert response_data["errors"] is None, content
        assert response_data["result"]["name"] == data["name"]
        assert response_data["result"]["summary"] == data["summary"]
        assert response_data["result"]["preferredSkills"] == data["preferredSkills"]

    def test_update_position(self):
        position = PositionFactory.create(
            name="Test Position",
            employment_type=EmployMentTypeEnum.TEMPORARY,
            summary="Summary",
            key_responsibilities="Responsibilities",
            qualifications="Qualifications",
            preferred_skills="Skills",
        )
        data = {
            "name": "Updated name",
            "summary": "Updated summary",
            "keyResponsibilities": "Updated responsibilities",
            "qualifications": "Updated Qualifications",
            "preferredSkills": "Updated Skills",
            "employmentType": EmployMentTypeEnum.FULL_TIME.name,
        }

        # Without authentication
        content = self._update_position_mutation(str(position.pk), data)
        assert content["data"]["updatePosition"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_position_mutation(str(position.pk), data)
        response_data = content["data"]["updatePosition"]
        assert response_data["errors"] is None, content

        position.refresh_from_db()
        assert response_data["result"]["name"] == position.name
        assert response_data["result"]["keyResponsibilities"] == position.key_responsibilities

    def test_archive_position(self):
        position = PositionFactory.create(
            name="Test Position",
            employment_type=EmployMentTypeEnum.TEMPORARY,
            summary="Summary",
            key_responsibilities="Responsibilities",
            qualifications="Qualifications",
            preferred_skills="Skills",
        )

        # Without authentication
        content = self._archive_position_mutation(str(position.pk))
        assert content["data"]["archivePosition"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_position_mutation(str(position.pk))
        response_data = content["data"]["archivePosition"]
        assert response_data["errors"] is None
        position.refresh_from_db()
        assert position.is_archived is True
