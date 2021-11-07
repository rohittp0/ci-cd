import json
import subprocess
import os

import requests
from django.db import models
from dotenv import load_dotenv

from status.constants import BASE_URL, TEST_PASSED, INTERNAL_ERROR, TEST_FAILED


class PullRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()
    from_branch = models.TextField()
    to_branch = models.TextField()
    repo = models.TextField()
    title = models.TextField()
    url = models.URLField()
    open = models.BooleanField(default=True)
    sha = models.TextField(max_length=40)
    test_output = models.TextField(default="")
    test_status = models.IntegerField(default=-1)

    class Meta:
        ordering = ['created_at']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.open:
            return super().save(force_insert, force_update, using, update_fields)

        load_dotenv()

        url = f"https://api.github.com/repos/{self.repo}/statuses/{self.sha}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'token {os.getenv("GIT_HUB_TOKEN")}'
        }

        requests.post(url, headers=headers, data=json.dumps({"state": "pending", "context": "The Ultimate Test"}))

        repo = f"git@github.com:{self.repo}"
        repo_name = self.repo.split("/")[1]
        branch = self.from_branch

        proc = subprocess.Popen(["sh", "test.sh", repo, repo_name, branch], stdout=subprocess.PIPE)
        result, err = proc.communicate()
        exit_code = proc.wait()

        self.test_status = exit_code
        self.test_output = (err or result).decode()

        super().save(force_insert, force_update, using, update_fields)

        result = json.dumps({
            "state": "success" if exit_code != 3 else "error",
            "context": "The Ultimate Test",
            "target_url": f"{BASE_URL}/{self.id}/output/",
            "description": [TEST_PASSED, INTERNAL_ERROR, INTERNAL_ERROR, TEST_FAILED][exit_code]
        })

        requests.post(url, headers=headers, data=result)
