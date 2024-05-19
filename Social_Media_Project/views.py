from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return HttpResponseRedirect(reverse('App_post:home'))