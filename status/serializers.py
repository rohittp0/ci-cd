from rest_framework import serializers
from status.models import PullRequest


class PullRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullRequest
        fields = ["id", "created_at", "created_by", "from_branch", "to_branch", "repo", "title", "url", "open"]
