# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import googlemaps
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView, View
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers
import json
from .models import UserProfile, Location, PanditProfile
from .forms import UserSignupForm


def index(request):
    return render(request, 'home.html')


class UserSignupView(FormView):
    template_name = "user_signup_form.html"
    form_class = UserSignupForm

    def form_valid(self, form):
        instance = form.save()
        location_name = form.cleaned_data.get('location_name')
        lat = form.cleaned_data.get('lat')
        lng = form.cleaned_data.get('lng')
        location_values = form.data.get('location_values').split(',')
        username = form.cleaned_data.get('username')
        contact = form.data.get('number')

        password = form.cleaned_data.get('password')
        instance.set_password(password)
        instance.save()
        location_list = list()
        if form.data.get('optradio') == 'pandit':
            user_object = PanditProfile.objects.create(
                    user=instance, contact=contact)

            for location in location_values:
                try:

                    location_object = Location.objects.get(name=location)
                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                    geocode_result = gmaps.geocode(location)
                    location_object.lat =  geocode_result[0]['geometry']['location']['lat']

                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                    geocode_result = gmaps.geocode(location)
                    location_object.lng =  geocode_result[0]['geometry']['location']['lng']

                    location_object.save()
                    location_list.append(location_object)
                except Location.DoesNotExist:
                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                    geocode_result = gmaps.geocode(location)
                    lat =  geocode_result[0]['geometry']['location']['lat']

                    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                    geocode_result = gmaps.geocode(location)
                    lng =  geocode_result[0]['geometry']['location']['lng']

                    location_object = Location.objects.create(name=location,
                        lat=lat,
                        lng=lng)
                    location_list.append(location_object)

                user_object.location.add(location_object)
                user_object.save()
        elif form.data.get('optradio') == 'user':
            try :
                location_object = Location.objects.get(name=location_name)
            except Location.DoesNotExist:
                location_object = Location.objects.create(name=location_name,
                    lat=lat,
                    lng=lng)
            UserProfile.objects.create(user=instance,
                location=location_object, contact=contact)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form":form})


class PanditSearchView(TemplateView):
    template_name = "includes/pandit_search.html"

    def get_context_data(self, user_id, *args, **kwargs):
        context = super(PanditSearchView, self).get_context_data(
            *args, **kwargs)
        user_object = UserProfile.objects.get(pk=user_id)
        pandits = PanditProfile.objects.filter(
                location__lat=user_object.location.lat,
                location__lng=user_object.location.lng)
        context['pandits'] = pandits
        return context

