from django.urls import include, path
from rest_framework import routers

from status.views import PullRequestViewSet

router = routers.DefaultRouter()
router.register(r'', PullRequestViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'', include(router.urls)),
]
