from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())