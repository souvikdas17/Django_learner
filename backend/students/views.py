from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def students(requests):
    return HttpResponse('<h2>Hello World</h2>')