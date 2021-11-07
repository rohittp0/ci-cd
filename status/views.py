from rest_framework import viewsets
from rest_framework.response import Response

from status.models import PullRequest
from status.serializers import PullRequestSerializer


class PullRequestViewSet(viewsets.ModelViewSet):
    methods = ["get", "post", "delete"]
    queryset = PullRequest.objects.all().order_by('created_at')
    serializer_class = PullRequestSerializer

    def create(self, request, *args, **kwargs):
        pull = request.data["pull_request"]
        data = {
            "title": pull["title"],
            "created_by": pull["user"]["login"],
            "from_branch": pull["head"]["ref"],
            "repo": pull["head"]["repo"]["full_name"],
            "to_branch": pull["base"]["ref"],
            "url": pull["_links"]["html"]["href"],
            "created_at": pull["created_at"],
            "open": request.data["action"] == "opened" or request.data["action"] == "reopened"
        }

        try:
            model = PullRequest.objects.get(url=data["url"])
            serializer = PullRequestSerializer(model, data=data)
        except Exception:
            serializer = PullRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(400)

        serializer.save()

        return Response(200)
