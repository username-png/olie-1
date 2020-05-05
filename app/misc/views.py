from django.http import HttpResponse
from django.views.generic import TemplateView

from .tasks import healthcheck as healthcheck_task


def healthcheck(request):
    healthcheck_task.send()
    return HttpResponse('healthy')


class LandingPageView(TemplateView):
    template_name = 'index.html'
