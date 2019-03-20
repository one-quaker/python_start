from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from .models import Post


class IndexView(generic.TemplateView):
    template_name = 'index.html'
