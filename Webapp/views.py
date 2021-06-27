from django.http import HttpResponse
from django.shortcuts import render , redirect

# Create your views here.
def home_get(request):
	request.session['user_id'] = 1
	return HttpResponse('HELO WEB APP SESSION SET')