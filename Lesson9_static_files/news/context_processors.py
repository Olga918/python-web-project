from django.conf import settings


def portal(request):
    return {
        'SITE_NAME': getattr(settings, 'PORTAL_SITE_NAME', 'Новинний портал'),
    }
