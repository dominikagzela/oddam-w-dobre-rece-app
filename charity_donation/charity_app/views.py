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
from charity_app.forms import RegisterUserForm, LoginUserForm
from charity_app.models import Category, Institution, Donation
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()


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


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd['email']
        password = cd['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        elif not User.objects.filter(username=username).exists():
            return HttpResponseRedirect(reverse_lazy('register'))
        else:
            return HttpResponse('Błędne dane logowania')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = form.cleaned_data
        email = cd['email']
        if User.objects.filter(username=email).exists():
            return HttpResponse('Użytkownik z takim mailem już istnieje!')

        password1 = cd['password1']
        password2 = cd['password2']
        if password1 != password2:
            return HttpResponse('Hasla nie są identyczne!')

        User.objects.create_user(
            username=cd['email'],
            first_name=cd['name'],
            last_name=cd['surname'],
            password=cd['password2'],
        )

        return super().form_valid(form)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')

