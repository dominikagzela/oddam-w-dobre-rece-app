from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.views.generic import (
    View,
    FormView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from charity_app.models import Category, Institution, Donation


class LandingPageView(View):
    def get(self, request):
        institutions = Institution.objects.all()
        number_of_organisations = institutions.count()
        number_of_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        ctx = {
            "number_of_bags": number_of_bags,
            "number_of_organisations": number_of_organisations,
        }
        return render(request, 'index.html', ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')

