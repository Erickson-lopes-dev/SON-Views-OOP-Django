from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Address
from .forms import AddressForm
from django.views.generic import TemplateView, View, RedirectView, ListView, DetailView, CreateView, UpdateView
from django_views_oop.settings import LOGIN_URL
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LoginView(TemplateView):
    template_name = 'my_app/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            django_login(request, user)
            # next_param = request.GET.get('next')
            # if next_param
            # return HttpResponseRedirect('/home/')
            return redirect('/home/')
        message = 'Credenciais inválidas'
        return self.render_to_response({'message': message})


# 302 - temporario
# 301 - permanente

# Para não ficar repetindo o @login_required(login_url='/login') em cada função
@method_decorator(login_required(login_url='/login'), name="dispatch")
class LogoutRedirectView(RedirectView):
    url = '/logout/'

    def get(self, request, *args, **kwargs):
        django_logout(request)
        return super().get(request, *args, **kwargs)


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    # queryset = Address.objects.filter()
    template_name = 'my_app/address/list.html'


class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address
    template_name = 'my_app/address/detail.html'


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    # fields = ['address', 'address_complement', 'city', 'state', 'country']
    form_class = AddressForm
    success_url = reverse_lazy('my_app:address_list')
    template_name = 'my_app/address/create.html'

    # validar e salvar
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    # fields = ['address', 'address_complement', 'city', 'state', 'country']
    form_class = AddressForm
    template_name = 'my_app/address/update.html'
    success_url = reverse_lazy('my_app:address_list')

    # validar e salvar
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, form_submitted=True))


@login_required(login_url='/login')
def home(request):
    return render(request, 'my_app/home.html')


# @login_required(login_url='/login')
# def address_create(request):
#     form_submitted = False
#     if request.method == 'GET':
#         form = AddressForm()
#     else:
#         form_submitted = True
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.user = request.user
#             address.save()
#
#             return redirect(reverse('my_app:address_list'))
#
#     return render(request, 'my_app/address/create.html', {'form': form, 'form_submitted': form_submitted})


@login_required(login_url=LOGIN_URL)
def address_update(request, id):
    form_submitted = False
    address = Address.objects.get(id=id)
    if request.method == 'GET':
        # states = STATES_CHOICES
        # form = AddressForm(address.__dict__)
        form = AddressForm(instance=address)
    else:
        form_submitted = True
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            # address.address = request.POST.get('address')
            # address.address_complement = request.POST.get('address_complement')
            # address.city = request.POST.get('address_complement')
            # address.state = request.POST.get('state')
            # address.country = request.POST.get('address_complement')
            # address.user = request.user

            # address.save()
            return redirect(reverse('my_app:address_list'))

    return render(request, 'my_app/address/update.html',
                  {'address': address, 'form': form, 'form_submitted': form_submitted})


@login_required(login_url='/login')
def address_destroy(request, id):
    address = Address.objects.get(id=id)
    if request.method == 'GET':
        form = AddressForm(instance=address)
    else:
        address.delete()
        return redirect(reverse('my_app:address_list'))

    return render(request, 'my_app/address/destroy.html', {'address': address, 'form': form})
