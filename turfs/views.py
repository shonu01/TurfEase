from django.shortcuts import render, get_object_or_404
from .models import Turf


def turf_list(request):
    turfs = Turf.objects.all().order_by('-created_at')
    return render(request, 'turf_list.html', {'turfs': turfs})


def turf_detail(request, pk):
    turf = get_object_or_404(Turf, pk=pk)
    return render(request, 'turf_detail.html', {'turf': turf})
