import json
import os

import requests
from dotenv import load_dotenv

from rest_framework.decorators import api_view

from rest_framework.response import Response


@api_view(["POST"])
def on_delete(request):
    load_dotenv()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {os.getenv("GIT_HUB_TOKEN")}'
    }

    repo_name = request.data['repository']['full_name']

    repo = requests.get(f"https://api.github.com/repos/{repo_name}", headers=headers).json()

    base = requests.get(f"https://api.github.com/repos/{repo_name}/git/refs/heads/{repo['default_branch']}",
                        headers=headers).json()

    requests.post(f"https://api.github.com/repos/{repo_name}/git/refs",
                  headers=headers,
                  data=json.dumps({"ref": f"refs/heads/{request.data['ref']}", "sha": base["object"]["sha"]}))

    return Response(200)
