from django.shortcuts import render

# Create your views here.

def members_management(request):
    return render(request, 'members.html', {})
