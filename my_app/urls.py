from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutRedirectView.as_view()),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/<int:pk>', views.AddressDetailView.as_view(), name='address_detail'),
    path('addresses/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('addresses/<int:pk>/update/', views.AddressUpdateView.as_view(), name='address_update'),
    path('addresses/<int:pk>/destroy/', views.AddressDestroyView.as_view(), name='address_destroy'),
]
