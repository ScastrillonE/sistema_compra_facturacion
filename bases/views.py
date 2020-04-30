from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView


# Create your views here.

class SinPrivilegiosTemplate(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'login'
    #raise_exception = False
    #redirect_field_name = 'redirec_to'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.login_url = 'sinprivilegios'
        else:
            self.login_url = 'login'
        return HttpResponseRedirect(reverse_lazy(self.login_url))




class Home(LoginRequiredMixin, TemplateView):
    template_name = 'bases/index.html'
    login_url = 'login'


class SinPrivilegios(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'bases/sinprivilegios.html'
