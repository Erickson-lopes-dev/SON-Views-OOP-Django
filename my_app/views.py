from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import Address
from .forms import AddressForm


# Create your views here.
def login(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'my_app/login.html')

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
    return render(request, 'my_app/login.html', {'message': message})

    # if request.user.is_authenticated():
    #     request.user.first_name
    #     #logica quando o usuario está autenticado


@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('/login/')


@login_required(login_url='/login')
def home(request):
    return render(request, 'my_app/home.html')


@login_required(login_url='/login')
def address_list(request):
    addresses = Address.objects.all()
    # print(list(addresses))
    return render(request, 'my_app/address/list.html', {'addresses': addresses})


@login_required(login_url='/login')
def address_create(request):
    form_submitted = False
    if request.method == 'GET':
        # states = STATES_CHOICES
        form = AddressForm()
    else:
        form_submitted = True
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return redirect(reverse('my_app:address_list'))

    return render(request, 'my_app/address/create.html', {'form': form, 'form_submitted': form_submitted})


@login_required(login_url='/login')
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