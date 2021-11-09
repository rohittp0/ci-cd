from rest_framework.decorators import api_view


# Create your views here.
@api_view(["POST"])
def on_delete(request):
    print(request.data)
    # default_branch
