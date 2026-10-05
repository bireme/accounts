from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.conf import settings

# form actions
ACTIONS = {
    'orderby': 'id',
    'order': '+',
    'page': 1,
    's': "",
}

def cookie_lang(request):

    language = (request.GET.get('language') or '').lower()
    if language not in dict(settings.LANGUAGES):
        return HttpResponseBadRequest("Invalid language")

    request.session[settings.LANGUAGE_COOKIE_NAME] = language

    response = HttpResponse(language)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )

    return response
