from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('login/', views.LoginView.as_view()),
    # path('login/', views.LoginView.as_view(template_name='my_app/home.html')),
    # path('logout/', views.logout),
    path('logout/', views.LogoutRedirectView.as_view()),
    path('home/', views.home),
    # path('addresses/', views.address_list, name='address_list'),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/<int:pk>', views.AddressDetailView.as_view(), name='address_detail'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/<int:id>/update/', views.address_update, name='address_update'),
    path('addresses/<int:id>/destroy/', views.address_destroy, name='address_destroy'),
]