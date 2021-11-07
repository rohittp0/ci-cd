from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status

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
            "sha": pull["head"]["sha"],
            "open": request.data["action"] == "opened" or request.data["action"] == "reopened"
        }

        try:
            model = PullRequest.objects.get(url=data["url"])
            serializer = PullRequestSerializer(model, data=data)
        except:
            serializer = PullRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="output")
    def get_build_output(self, request, pk):
        try:
            pull = self.queryset.get(id=pk)
            return HttpResponse(
                f"<h3>Output</h3><pre><code>{pull.test_output}</code></pre> <h4>Status</h4><h5>{pull.test_status}</h5>")
        except Exception:
            return Response(status.HTTP_404_NOT_FOUND)
