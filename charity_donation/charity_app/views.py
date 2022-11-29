import random

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import (
    View,
    FormView,
    ListView,
    RedirectView,
    UpdateView,
)
from charity_app.forms import (
    RegisterUserForm,
    LoginUserForm,
    DonationForm,
    ChangePasswordForm,
    UserProfileForm,
    ConfirmPasswordForm,
    IfDonationTakenForm,
)
from charity_app.models import Category, Institution, Donation
from django.core.paginator import Paginator
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
            user = request.user

            institution = cd['institution']
            institution_instance = Institution.objects.get(name=institution)

            categories = cd['categories']
            list_categories = []
            for category in categories:
                current_category = Category.objects.get(name=category)
                list_categories.append(current_category)

            donation = Donation.objects.create(
                quantity=cd['quantity'],
                institution=institution_instance,
                address=cd['address'],
                phone_number=cd['phone_number'],
                city=cd['city'],
                zip_code=cd['zip_code'],
                pick_up_date=cd['pick_up_date'],
                pick_up_time=cd['pick_up_time'],
                pick_up_comment=cd['pick_up_comment'],
                user=user,
            )
            donation.categories.set(list_categories)
            return HttpResponseRedirect(reverse_lazy('confirmation'))
        return HttpResponseRedirect(reverse_lazy('add-donation'))


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfileView(UpdateView):
    model = Donation
    template_name = 'user-profile.html'
    form_class = IfDonationTakenForm
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        user = self.request.user
        current_user = User.objects.get(id=user.id)
        user_donations = Donation.objects.filter(user=user.id).order_by('is_taken')

        ctx = {
            'current_user': current_user,
            "user_donations": user_donations,
        }
        return ctx

    def post(self, request, *args, **kwargs):
        is_taken = request.POST.get('is_taken')
        id = request.POST.get('id')
        current_donation = Donation.objects.get(id=int(id))
        print(id, type(id))
        print(current_donation, type(current_donation.is_taken))
        if is_taken == 'Niezabrany':
            current_donation.is_taken = False
        else:
            current_donation.is_taken = True
        current_donation.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        user = self.request.user
        return reverse('user_profile', args=[user.id])


class SettingsView(ListView):

    model = User
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        current_user = User.objects.get(id=user.id)

        ctx = {
            'current_user': current_user,
        }
        return ctx


class UpdateUserProfileView(UpdateView):

    model = User
    template_name = 'update-profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('settings')
    pk_url_kwarg = 'user_id'


class ChangePasswordView(PasswordChangeView):

    template_name = 'change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('settings')


class ConfirmPasswordView(UpdateView):

    model = User
    template_name = 'confirm-password.html'
    form_class = ConfirmPasswordForm
    pk_url_kwarg = 'user_id'

    def get_success_url(self, *args, **kwargs):
        user = self.request.user
        return reverse('update-profile', args=[user.id])
