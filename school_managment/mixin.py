from django.shortcuts import redirect


# authenticated user dont have access
class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:home")
        return super().dispatch(request, *args, **kwargs)
