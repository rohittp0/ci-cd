import json
import subprocess
import os

import requests
from celery import shared_task
from status.constants import BASE_URL, TEST_PASSED, TEST_FAILED, headers

from status.models import PullRequest
from status.tests import test_with_yarn, send_status


def start_test_script(repo, repo_name, branch, model, post_params):
    home = "/home/user/"

    user = subprocess.run(["whoami"], capture_output=True, cwd=home)
    output = f"Running tests as {(user.stderr or user.stdout).decode()}\n"

    send_status(output, post_params)

    if not os.path.exists(os.path.join("/home/user/", repo_name)):
        clone = subprocess.run(["git", "clone", repo], capture_output=True, cwd=home)
        output += (clone.stderr or clone.stdout).decode() + "\n"
    else:
        output += "Repo already cloned"

    fetch = subprocess.run(["git", "fetch", "-p"], capture_output=True, cwd=os.path.join(home, repo_name))
    switch = subprocess.run(["git", "switch", branch], capture_output=True, cwd=os.path.join(home, repo_name))
    pull = subprocess.run(["git", "pull"], capture_output=True, cwd=os.path.join(home, repo_name))
    output += "\n".join([(proc.stderr or proc.stdout).decode() for proc in [fetch, switch, pull]])

    model.test_output = output
    model.save()

    send_status("Repo cloned", post_params)

    if os.path.exists(os.path.join("/home/user/", repo_name, "package.json")):
        exit_code = test_with_yarn(os.path.join(home, repo_name), model, post_params)
    else:
        model.test_output += "\nUnknown project type, passing blindly."
        exit_code = 0

    model.test_status = exit_code
    model.save()

    return exit_code


@shared_task
def run_test(model_id, rerun=False):
    model = PullRequest.objects.get(id=model_id)

    if (not model.open or not model.test_status == -1) and not rerun:
        return None

    url = f"https://api.github.com/repos/{model.repo}/statuses/{model.sha}"

    requests.post(url, headers=headers,
                  data=json.dumps({"state": "pending", "context": "The Ultimate Test", "description": "Running"}))

    repo = f"git@github.com:{model.repo}"
    repo_name = repo.split("/")[1]

    try:
        exit_code = start_test_script(repo, repo_name, model.from_branch, model, [headers, url])
    except Exception as err:
        exit_code = 1
        model.test_status = 1
        model.test_output += str(err)
        model.save()

    result = json.dumps({
        "state": "success" if exit_code == 0 else "error",
        "context": "The Ultimate Test",
        "target_url": f"{BASE_URL}/{model_id}/output/",
        "description": TEST_PASSED if exit_code == 0 else TEST_FAILED
    })

    return requests.post(url, headers=headers, data=result)
