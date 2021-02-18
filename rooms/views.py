from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.http import Http404

from django_countries import countries

from rooms import forms, models as room_models

# Create your views here.

PAGE_SIZE = 10


class HomeView(ListView):
    """ HomeView class definition """
    model = room_models.Room
    ordering = ["created"]
    paginate_by = PAGE_SIZE
    page_kwarg = "page"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDetail(DetailView):
    """ RoomDetail class definition """
    model = room_models.Room


def room_detail(request, pk):
    """ room_detail function definition """
    try:
        room = room_models.Room.objects.get(pk=pk)
    except room_models.Room.DoesNotExist:
        raise Http404()

    print(room)
    return render(request=request, template_name="rooms/room_detail.html",
                  context={"room": room}
                  )

#region SearchView
class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        print(request.GET)

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")

                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")

                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}



                if country is not None:
                    filter_args["country"] = country

                if city is not None and city != "Anywhere":
                    filter_args["city__startswith"] = city

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                qs = room_models.Room.objects.filter(**filter_args)

                if False:
                    for amenity in amenities:
                        qs = qs.filter(amenities=amenity)

                    for facility in facilities:
                        qs = qs.filter(facilities=facility)

                qs = qs.order_by("-created")

                paginator = Paginator(qs, 10, orphans=5, allow_empty_first_page=True)

                page = int(request.GET.get("page", 1))

                print("pagin")

                rooms = paginator.get_page(page)
                return render(
                    request,
                    "rooms/room_search.html",
                    {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/room_search.html",
            {"form": form}
        )
#endregion

def search(request):
    """ search function definition """

    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")

            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")

            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}
            if country != "0":
                filter_args["country"] = country

            if city != "Amywhere":
                filter_args["city__startswith"] = city

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            rooms = room_models.Room.objects.filter(**filter_args)

            for amenity in amenities:
                rooms = rooms.filter(amenities=int(amenity))

            for facility in facilities:
                rooms = rooms.filter(facilities=int(facility))
                    
    else:
        form = forms.SearchForm()


    return render(
        request,
        "rooms/room_search.html",
        {"form": form}
    )


"""
def all_rooms(request):
    page = request.GET.get('page', 1)
    if not page:
        return redirect(to="/")
    try:
        page_size = int(request.GET.get("page_size", PAGE_SIZE))
    except ValueError:
        page_size = PAGE_SIZE

    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, page_size)
    try:
        page = paginator.page(int(page))

    except EmptyPage:
        return redirect(to="/")

    my_context = {
        "page": page,
        "now": datetime.now(),
        "name": "Alex"
    }
    return render(request=request, template_name="rooms/home.html", context=my_context)
"""


"""

    city = request.GET.get("city", 0)
    city = str.capitalize(city)
    country = request.GET.get("country", "RU")
    room_type = int(request.GET.get("room_type", 0))

    print("fff", request.GET.get("price", 0) or 0, "fff")
    price = int(request.GET.get("price", 0) or 0)
    guests = int(request.GET.get("guests", 0) or 0)
    bedrooms = int(request.GET.get("bedrooms", 0) or 0)
    beds = int(request.GET.get("beds", 0) or 0)
    baths = int(request.GET.get("baths", 0) or 0)

    instant = request.GET.get("instant", False)
    superhost = request.GET.get("super_host", False)

    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")


    print(request.GET)
    print(s_amenities)
    form = {
            "city": city,
            "s_country": country,
            "s_room_type": room_type,
            "instant": instant,
            "superhost": superhost,
            "s_amenities": s_amenities,
            "s_facilities": s_facilities
    }

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()


    choices = {
            "countries": countries,
            "room_types": room_types,
            "amenities": amenities,
            "facilities": facilities
    }

    filter_args = {}

    if country != "0":
        filter_args["country"] = country

    if city != "Amywhere":
        filter_args["city__startswith"] = city

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type
   
    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = room_models.Room.objects.filter(**filter_args)

    if len(s_amenities) !=0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) != 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    num_inputs = [
        {"value": 0, "name": "min_price", "label": "Minimum Price"},
        {"value": -1, "name": "max_price", "label": "Maximum Price"}
    ]

    context = {
        "num_inputs": num_inputs,
        "rooms": rooms,
         ** form, **choices
    }

"""
