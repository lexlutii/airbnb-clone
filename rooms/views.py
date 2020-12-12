from math import ceil
from datetime import datetime

from django.shortcuts import render
from django.core.paginator import Paginator

from rooms import models as room_models

# Create your views here.

PAGE_SIZE = 10


def all_rooms(request):
    page = request.GET.get('page')
    try:
        page_size = int(request.GET.get("page_size", PAGE_SIZE))
    except ValueError:
        page_size = PAGE_SIZE

    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, page_size)
    page = paginator.get_page(page)
    my_context = {
        "page": page,
        "now": datetime.now(),
        "name": "Alex"
    }
    return render(request=request, template_name="rooms/home.html", context=my_context)
