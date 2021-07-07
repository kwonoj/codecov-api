from asgiref.sync import sync_to_async

from codecov_auth.models import Session
from codecov.commands.base import BaseInteractor
from compare.models import CommitComparison
from services.task import TaskService


class CompareCommits(BaseInteractor):
    def get_or_create_comparison(head_commit, compare_to_commit):
        return CommitComparison.objects.get_or_create(
            base_commit=head_commit, compare_commit=compare_to_commit
        )

    def trigger_task(self, comparison):
        TaskService().compute_comparison(comparison.id)

    @sync_to_async
    async def execute(self, head_commit, compare_to_commit):
        comparison, created = self.get_or_create_comparison(
            head_commit, compare_to_commit
        )
        if created:
            self.trigger_task(comparison)
        return comparison
