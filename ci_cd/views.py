from django.shortcuts import render

from status.models import PullRequest


def index(request):
    return render(request, 'ci_cd/index.html', {"pulls": PullRequest.objects.all()})
