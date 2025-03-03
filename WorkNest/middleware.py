from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from WorkNest import settings
from recrutare.models import Logs

class RefreshMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                new_instance = Logs()
                new_instance.user_id = request.user.id
                new_instance.actiunea = 'refresh'
                new_instance.url = request.path
                if 'stergere_pozitie' in new_instance.url:
                    new_instance.actiunea = 'stergere pozitie'
                if 'reactivare_pozitie' in new_instance.url:
                    new_instance.actiunea = 'reactivare pozitie'
                new_instance.save()
            elif request.method == "POST":
                action = 'creat'
                for item in str(request.path):
                    if item.isdigit():
                        action = 'modificat'
                        break
                Logs.objects.create(user_id=request.user.id, actiunea=action, url=request.path)
        return self.get_response(request)


class RedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/':
            return HttpResponseRedirect(reverse('candidati:recrutare'))
        return self.get_response(request)


class SessionTimeoutMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.timp_delogare = getattr(settings, 'SESSION_TIMEOUT_MINUTES', 5)

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.session is not None:
                timp_ultima_activitate = request.session.get('session_timeout_last_active')
                timp_curent = now()
                if timp_ultima_activitate:
                    timp_ultima_activitate = parse_datetime(timp_ultima_activitate)
                    if timp_ultima_activitate:
                        timp_inactiv = (timp_curent - timp_ultima_activitate).total_seconds() / 60
                        if timp_inactiv > self.timp_delogare:
                            logout(request)
                            return redirect('login')
                request.session['session_timeout_last_active'] = timp_curent.isoformat()
        response = self.get_response(request)
        return response


class Redirect404ToLoginMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return redirect('login')
        return response
