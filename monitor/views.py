from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from .models import Service


def service_list(request):
    services = Service.objects.order_by('-last_checked')
    return render(request, 'service_list.html', {'services': services})


def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect(service_list)
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})


def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect(service_list)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'add_service.html', {'form': form, 'edit': True})


def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, user=request.user)
    if request.method == 'POST':
        service.delete()
        return redirect(service_list)
    return render(request, 'delete_service.html', {'service': service})