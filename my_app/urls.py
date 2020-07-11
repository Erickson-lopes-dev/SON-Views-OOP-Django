from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/<int:id>/update/', views.address_update, name='address_update'),
    path('addresses/<int:id>/destroy/', views.address_destroy, name='address_destroy'),
]