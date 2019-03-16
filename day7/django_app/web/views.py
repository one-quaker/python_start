from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from .models import Donation


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class TopDonationView(generic.TemplateView):
    template_name = 'top_donation.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['top_donator_list'] = Donation.get_top()
        return ctx


class ApiTopList(generic.View):
    def calc_reward(self, amount):
        d = None
        if amount > 10:
            pass
        return d

    def get(self, request):
        data = dict(top_list=list(Donation.get_top()))
        return JsonResponse(data)
