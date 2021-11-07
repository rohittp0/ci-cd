from django.contrib import admin

# Register your models here.
from status.models import PullRequest

admin.register(PullRequest)
