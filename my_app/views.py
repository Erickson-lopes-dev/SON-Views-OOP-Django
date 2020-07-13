from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Address
from .forms import AddressForm
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


@method_decorator(login_required(login_url='/login'), name="dispatch")
class LogoutRedirectView(RedirectView):
    url = '/logout/'

    def get(self, request, *args, **kwargs):
        django_logout(request)
        return super().get(request, *args, **kwargs)


class FormSubmettiendInContexMixin():
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, form_submitted=True))


class LoginView(TemplateView):
    template_name = 'my_app/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            django_login(request, user)
            return redirect('/home/')
        message = 'Credenciais inválidas'
        return self.render_to_response({'message': message})


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    # queryset = Address.objects.filter()
    template_name = 'my_app/address/list.html'


class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address
    template_name = 'my_app/address/detail.html'


class AddressCreateView(LoginRequiredMixin, FormSubmettiendInContexMixin, CreateView):
    model = Address
    # fields = ['address', 'address_complement', 'city', 'state', 'country']
    form_class = AddressForm
    success_url = reverse_lazy('my_app:address_list')
    template_name = 'my_app/address/create.html'

    # validar e salvar
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, FormSubmettiendInContexMixin, UpdateView):
    model = Address
    # fields = ['address', 'address_complement', 'city', 'state', 'country']
    form_class = AddressForm
    template_name = 'my_app/address/update.html'
    success_url = reverse_lazy('my_app:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressDestroyView(DeleteView, LoginRequiredMixin):
    model = Address
    template_name = 'my_app/address/destroy.html'
    success_url = reverse_lazy('my_app:address_list')

