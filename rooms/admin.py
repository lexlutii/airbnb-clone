from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country",
                        "address", "room_type", "price")}
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out",
                        "instant_book")}
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")}
        ),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")}
        ),
        (
            "Last Details", {
                "fields": ("host",)
            }
        )
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",

        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities"
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "country",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("=city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules"
    )

    def count_amenities(self, obj):
        print(obj.amenities.all())
        return obj.amenities.count()

    count_amenities.short_description = "Amenities count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """
    pass
