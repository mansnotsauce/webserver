from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from boards.models import Result

@login_required
def home(request):
    allResults = Result.objects.all()
    user = request.user
    filteredResults = allResults.filter(user=user) 
    return render(request, 'home.html', {'results': filteredResults})
