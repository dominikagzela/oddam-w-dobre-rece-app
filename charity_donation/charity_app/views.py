import random

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
from django.core.paginator import Paginator


class LandingPageView(View):
    def get(self, request):
        institutions = Institution.objects.all()
        number_of_organisations = institutions.count()
        number_of_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']

        list_of_foundations = list(Institution.objects.filter(type=1))
        random.shuffle(list_of_foundations)
        paginator_foundations = Paginator(list_of_foundations, 3)
        page1 = request.GET.get('page1')
        three_foundations = paginator_foundations.get_page(page1)

        list_of_organisations = list(Institution.objects.filter(type=2))
        random.shuffle(list_of_organisations)
        paginator_organisations = Paginator(list_of_organisations, 3)
        page2 = request.GET.get('page2')
        three_organisations = paginator_organisations.get_page(page2)

        list_of_local_organisations = list(Institution.objects.filter(type=3))
        random.shuffle(list_of_local_organisations)
        paginator_local_organisations = Paginator(list_of_local_organisations, 3)
        page3 = request.GET.get('page3')
        three_local_organisations = paginator_local_organisations.get_page(page3)

        ctx = {
            "number_of_bags": number_of_bags,
            "number_of_organisations": number_of_organisations,
            "three_foundations": three_foundations,
            "three_organisations": three_organisations,
            "three_local_organisations": three_local_organisations,
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

