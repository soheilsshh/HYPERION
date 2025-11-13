# monitoring/views.py
from django.shortcuts import render, redirect
from .forms import ServiceForm
from .models import Service


def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'monitoring/add_service.html', {'form': form})


def service_list(request):
    services = Service.objects.filter(user=request.user)
    return render(request, 'monitoring/list.html', {'services': services})