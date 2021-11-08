import json
import subprocess
import os

import requests
from celery import shared_task
from dotenv import load_dotenv
from status.constants import BASE_URL, TEST_PASSED, INTERNAL_ERROR, TEST_FAILED

from status.models import PullRequest


@shared_task
def run_test(model_id, rerun=False):
    model = PullRequest.objects.get(id=model_id)

    if (not model.open or not model.test_status == -1) and not rerun:
        return None

    load_dotenv()
    url = f"https://api.github.com/repos/{model.repo}/statuses/{model.sha}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {os.getenv("GIT_HUB_TOKEN")}'
    }

    requests.post(url, headers=headers,
                  data=json.dumps({"state": "pending", "context": "The Ultimate Test", "description": "Running"}))

    repo = f"git@github.com:{model.repo}"
    repo_name = repo.split("/")[1]

    proc = subprocess.Popen(["sh", "test.sh", repo, repo_name, model.from_branch], stdout=subprocess.PIPE)
    result, err = proc.communicate()
    exit_code = proc.wait()

    model.test_status = exit_code
    model.test_output = (err or result).decode()
    model.save()

    result = json.dumps({
        "state": "success" if exit_code != 3 else "error",
        "context": "The Ultimate Test",
        "target_url": f"{BASE_URL}/{model_id}/output/",
        "description": [TEST_PASSED, INTERNAL_ERROR, INTERNAL_ERROR, TEST_FAILED][exit_code]
    })

    return requests.post(url, headers=headers, data=result)
