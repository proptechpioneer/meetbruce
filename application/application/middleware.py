from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, 'CANONICAL_HOST', '')
        enforce_canonical_host = getattr(settings, 'ENFORCE_CANONICAL_HOST', False)

        if canonical_host and enforce_canonical_host:
            request_host = request.get_host().split(':', 1)[0]
            if request_host and request_host != canonical_host:
                redirect_url = f"{request.scheme}://{canonical_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(redirect_url)

        return self.get_response(request)