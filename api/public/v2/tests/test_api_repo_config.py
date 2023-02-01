from unittest.mock import patch

from django.urls import reverse
from freezegun import freeze_time

from codecov.tests.base_test import InternalAPITest
from codecov_auth.tests.factories import OwnerFactory
from core.tests.factories import RepositoryFactory


@freeze_time("2022-01-01T00:00:00")
class RepoConfigViewTests(InternalAPITest):
    def setUp(self):
        self.org = OwnerFactory()
        self.repo = RepositoryFactory(author=self.org)
        self.user = OwnerFactory(
            permission=[self.repo.repoid], organizations=[self.org.ownerid]
        )
        self.client.force_login(user=self.user)

    @patch("api.shared.repo.repository_accessors.RepoAccessors.get_repo_permissions")
    def test_get(self, get_repo_permissions):
        get_repo_permissions.return_value = (True, True)

        res = self.client.get(
            reverse(
                "api-v2-repo-config",
                kwargs={
                    "service": self.org.service,
                    "owner_username": self.org.username,
                    "repo_name": self.repo.name,
                },
            )
        )
        assert res.status_code == 200
        assert res.json() == {
            "upload_token": self.repo.upload_token,
        }

    @patch("api.shared.repo.repository_accessors.RepoAccessors.get_repo_permissions")
    def test_get_no_part_of_org(self, get_repo_permissions):
        get_repo_permissions.return_value = (True, True)

        self.user.organizations = []
        self.user.save()

        res = self.client.get(
            reverse(
                "api-v2-repo-config",
                kwargs={
                    "service": self.org.service,
                    "owner_username": self.org.username,
                    "repo_name": self.repo.name,
                },
            )
        )
        assert res.status_code == 403
        assert self.repo.upload_token not in str(res.content)