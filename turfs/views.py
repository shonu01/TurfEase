from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from .models import Turf


def turf_list(request):
    turfs = Turf.objects.all().order_by('-created_at')

    # Search by name or location
    search = request.GET.get('q', '')
    if search:
        turfs = turfs.filter(
            models.Q(name__icontains=search) | models.Q(location__icontains=search)
        )

    paginator = Paginator(turfs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'turf_list.html', {'page_obj': page_obj, 'search': search})


def turf_detail(request, pk):
    turf = get_object_or_404(Turf, pk=pk)
    return render(request, 'turf_detail.html', {'turf': turf})
