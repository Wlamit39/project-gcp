def submit_exception_on_sentry():
    from raven.contrib.django.raven_compat.models import client as raven_client
    raven_client.captureException()