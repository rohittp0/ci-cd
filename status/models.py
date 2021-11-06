from django.db import models


class PullRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(max_length=15)
    from_branch = models.TextField(max_length=10)
    to_branch = models.TextField(max_length=10)

    class Meta:
        ordering = ['created_at']
        
