from django import forms

from django_countries.fields import CountryField

from . import models


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="RU").formfield()
    room_type = forms.ModelChoiceField(
        empty_label="Any kind", queryset=models.RoomType.objects.all(),
        required=False
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False, help_text="How many people will be staying?")
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(), required=False,
        widget= forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(), required=False, 
        widget= forms.CheckboxSelectMultiple
    )


"""
    <div>
        <label for="city">City</label>
        <input value="{{city}}" id="city" name="city" placeholder="Search by City">
    </div>
    <div>
        <label for="country">Country</label>
        <select id="country" name="country">
            <option value="0">Anywhere</option>            
            {% for country in countries %}
                <option value="{{country.code}}" {% if country.code == s_country %} selected{% endif %}>{{country.name}}</option>
            {% endfor %}
                
        </select>
    </div>
    <div>
        <label for="room_type">Room Type</label>
        <select id="room_type" name="room_type">
            <option value="0"{% if s_room_type == "0" %} selected{% endif %}>Any kind</option>
            {% for room_type in room_types %}
            <option value="{{room_type.pk}}"{% if s_room_type == room_type %} selected{% endif %}>{{room_type.name}}</option>
            {% endfor %}
    
        </select>
    </div>

    {% for num_input in num_inputs %}
        <div>
            <label for="{{num_input.name}}">{{num_input.label}}</label>
            <input value="{{num_input.value}}" type="number" name="{{num_input.name}}" id="{{num_input.name}}" placeholder="{{num_input.label}}">
        </div>
    {% endfor %}


    <div>
        <label for="price">Price</label>
        <input type="number" name="price" id="price" placeholder="Price">
    </div>
    <div>
        <label for="guests">Guests</label>
        <input type="number" name="guests" id="guests" placeholder="Guests">
    </div>
    <div>
        <label for="bedrooms">Bedrooms</label>
        <input type="number" name="bedrooms" id="bedrooms" placeholder="Bedrooms">
    </div>
    <div>
        <label for="beds">Guests</label>
        <input type="number" name="guests" id="guests" placeholder="Guests">
    </div>

    <div>
        <label for="superhost">By Superhost Only?</label>
        <input 
            type="checkbox" name="superhost" 
            id="superhost" {% if superhost %}checked{% endif %}
        />
    </div>
    <div>
        <label for="instant">Instant Book Only?</label>
        <input 
            type="checkbox" name="instant" 
            id="instant"  {% if instant %}checked{% endif %}
        />
    </div>
        
    <div>
        <h3>Amenities</h3>
        <ul>
            {% for amenity in amenities %}
                <li>
                    <label for="a_{{amenity.pk}}">{{amenity.name}}</label>
                    <input 
                    id="a_{{amenity.pk}}" 
                    name="amenities" 
                    type="checkbox" 
                    value="{{amenity.pk}}" 
                    {% if amenity.pk|slugify in s_amenities %}checked{% endif %}
                    />
                </li>
            {% endfor %}
        </ul>
    </div>
    <div>
        <h3>Facilities</h3>
        <ul>
            {% for facility in facilities %}
                <li>
                    <label for="f_{{facility.pk}}">{{facility.name}}</label>
                    <input 
                        id="f_{{facility.pk}}" 
                        name="facility" 
                        type="checkbox" 
                        value="{{facility.pk}}"
                        {% if facility.pk|slugify in s_facilities %}checked{% endif %}
                    />
                </li>
            {% endfor %}
        </ul>
    </div>

"""
