from rest_framework import serializers

from profiling.models import ProfilingCommit, ProfilingUpload
from services.archive import ArchiveService


class CreatableProfilingCommitRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        # this will be a problem once we start having a tokens capable
        # of sending data to multiple repos, because of
        # the uniqueness of (repoid, code) pair
        return ProfilingCommit.objects.filter(
            repository__in=self.context["request"].auth.get_repositories()
        )


class ProfilingUploadSerializer(serializers.ModelSerializer):
    raw_upload_location = serializers.SerializerMethodField()
    profiling = CreatableProfilingCommitRelatedField(
        slug_field="code", source="profiling_commit"
    )

    class Meta:
        fields = ("raw_upload_location", "profiling", "created_at", "external_id")
        read_only_fields = ("created_at", "raw_upload_location", "external_id")
        model = ProfilingUpload

    def get_raw_upload_location(self, obj):
        repo = obj.profiling_commit.repository
        archive_service = ArchiveService(repo)
        return archive_service.create_presigned_put(obj.raw_upload_location)


class ProfilingCommitSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)

    class Meta:
        model = ProfilingCommit
        fields = (
            "created_at",
            "external_id",
            "code",
            "environment",
            "version_identifier",
        )
        read_only_fields = ("created_at", "external_id")
