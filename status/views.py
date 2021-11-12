import requests
from django.db.models.signals import post_save
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.dispatch import receiver
from django.db.backends.signals import connection_created

from status.constants import headers
from status.models import PullRequest
from status.serializers import PullRequestSerializer
from status.task import run_test


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
            "open": request.data["action"] == "opened" or request.data["action"] == "reopened",
            "test_status": -1
        }

        try:
            model = PullRequest.objects.get(url=data["url"])
            data["test_status"] = -1 if data["open"] else model.test_status

            serializer = PullRequestSerializer(model, data=data)
        except PullRequest.DoesNotExist:
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
        except PullRequest.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    @action(methods=["get"], detail=True, url_path="rerun", permission_classes=[permissions.IsAuthenticated])
    def rerun(self, request, pk):
        run_test.delay(pk, rerun=True)
        return HttpResponse("<h4>Re-running tests</h4>")


@receiver(post_save, sender=PullRequest)
def on_save(sender, instance, **kwargs):
    if instance.open:
        run_test.delay(instance.id)


@receiver(connection_created)
def on_connection(connection, **kwargs):
    repos = set(PullRequest.objects.values_list('repo', flat=True))

    for repo in repos:
        for pull in requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers).json():
            if pull["state"] != "open" or PullRequest.objects.all().filter(url=pull["_links"]["html"]["href"]).exists():
                continue

            data = {
                "title": pull["title"],
                "created_by": pull["user"]["login"],
                "from_branch": pull["head"]["ref"],
                "repo": pull["head"]["repo"]["full_name"],
                "to_branch": pull["base"]["ref"],
                "url": pull["_links"]["html"]["href"],
                "created_at": pull["created_at"],
                "sha": pull["head"]["sha"],
                "open": True,
                "test_status": -1
            }

            serializer = PullRequestSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
