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
from charity_app.forms import RegisterUserForm, LoginUserForm, DonationForm
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
        page1 = request.GET.get('page1', 1)
        three_foundations = paginator_foundations.get_page(page1)

        list_of_organisations = list(Institution.objects.filter(type=2))
        random.shuffle(list_of_organisations)
        paginator_organisations = Paginator(list_of_organisations, 3)
        page2 = request.GET.get('page2', 1)
        three_organisations = paginator_organisations.get_page(page2)

        list_of_local_organisations = list(Institution.objects.filter(type=3))
        random.shuffle(list_of_local_organisations)
        paginator_local_organisations = Paginator(list_of_local_organisations, 3)
        page3 = request.GET.get('page3', 1)
        three_local_organisations = paginator_local_organisations.get_page(page3)

        active_page = request.GET.get('active_page', '1')

        ctx = {
            "number_of_bags": number_of_bags,
            "number_of_organisations": number_of_organisations,
            "three_foundations": three_foundations,
            "three_organisations": three_organisations,
            "three_local_organisations": three_local_organisations,
            "active_page": active_page,
            "page1": int(page1),
            "page2": int(page2),
            "page3": int(page3),
        }
        return render(request, 'index.html', ctx)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd['email'],
            first_name=cd['name'],
            last_name=cd['surname'],
            password=cd['password2'],
            email=cd['email'],
        )
        return super().form_valid(form)


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
        if User.objects.filter(username=username).exists():
            return HttpResponseRedirect(reverse_lazy('register'))


class LogoutView(RedirectView):
    url = reverse_lazy('landing-page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# class AddDonationView(FormView):
#     template_name = 'form.html'
#     form_class = DonationForm
#     success_url = reverse_lazy('confirmation')
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             categories = Category.objects.all().order_by('name')
#             institutions = Institution.objects.all().order_by('name')
#             ctx = {
#                 "categories": categories,
#                 "institutions": institutions,
#             }
#             return render(request, 'form.html', ctx)
#         else:
#             return HttpResponseRedirect(reverse_lazy('login'))
#
#     def form_valid(self, request, form):
#         cd = form.cleaned_data
#         user = request.user
#         print('bags: ', cd['bags'])
#         print('categories: ', cd['categories'])
#         print('institution: ', cd['institution'])
#         print('address: ', cd['address'])
#         print('phone: ', cd['phone'])
#         print('city: ', cd['city'])
#         print('postcode: ', cd['postcode'])
#         print('date: ', cd['date'])
#         print('time: ', cd['time'])
#         print('more_info: ', cd['more_info'])
#         print('user: ', user)
#
#         Donation.objects.create(
#             quantity=cd['bags'],
#             categories=cd['categories'],
#             institution=cd['institution'],
#             address=cd['address'],
#             phone_number=cd['phone'],
#             city=cd['city'],
#             zip_code=cd['postcode'],
#             pick_up_date=cd['date'],
#             pick_up_time=cd['time'],
#             pick_up_comment=cd['more_info'],
#             user=user,
#         )
#         return super().form_valid(form)

class AddDonationView(View):
    template_name = 'form.html'
    form_class = DonationForm
    success_url = reverse_lazy('confirmation')

    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all().order_by('name')
            institutions = Institution.objects.all().order_by('name')
            form = self.form_class()
            ctx = {
                "categories": categories,
                "institutions": institutions,
                "form": form
            }
            return render(request, 'form.html', ctx)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # user = request.user
            user = 3
            print('bags: ', cd['quantity'])
            print('categories: ', cd['categories'])
            print('institution: ', cd['institution'])
            print('address: ', cd['address'])
            print('phone: ', cd['phone_number'])
            print('city: ', cd['city'])
            print('postcode: ', cd['zip_code'])
            print('date: ', cd['pick_up_date'])
            print('time: ', cd['pick_up_time'])
            print('more_info: ', cd['pick_up_comment'])
            print('user: ', user)

            Donation.objects.create(
                quantity=cd['quantity'],
                categories=cd['categories'],
                institution=cd['institution'],
                address=cd['address'],
                phone_number=cd['phone_number'],
                city=cd['city'],
                zip_code=cd['zip_code'],
                pick_up_date=cd['pick_up_date'],
                pick_up_time=cd['pick_up_time'],
                pick_up_comment=cd['pick_up_comment'],
                user=user,
            )
        # ctx = {'form': form}
        # return render(request, 'form.html', ctx)
            return HttpResponseRedirect(reverse_lazy('confirmation'))
        return HttpResponseRedirect(reverse_lazy('login'))


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfileView(ListView):
    model = User
    template_name = 'user-profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        current_user = User.objects.get(id=user.id)
        user_donation = Donation.objects.get(user=user.id)

        ctx = {
            'current_user': current_user,
            "user_donation": user_donation
        }
        return ctx
