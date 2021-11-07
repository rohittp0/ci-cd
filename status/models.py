from django.db import models


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
        super().save(force_insert, force_update, using, update_fields)
