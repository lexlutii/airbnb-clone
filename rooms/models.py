from django.db import models

from django_countries.fields import CountryField

from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):
    """"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    class Meta:
        verbose_name = "Room type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity object definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"
        verbose_name_plural = "House Rules"


class Photo(core_models.TimeStampedModel):
    """ Photo model definition """

    caption = models.CharField(max_length=140)
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "Photo"


class Room(core_models.TimeStampedModel):
    """ Room Model Defenition"""

    name = models.CharField(max_length=140)
    desctiption = models.TextField()
    contry = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()

    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_riles = models.ManyToManyField(HouseRule, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rooms"
