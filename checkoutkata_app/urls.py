from django.urls import path
from .views import *


urlpatterns = [
    path('', dologin, name='login'),
    path('login/', dologin, name='login'),
    path('signup/', signup, name='signup'),
    path('shopowner_dashboard/', shopowner_dashboard, name='shopowner_dashboard'),
    path('customer_dashboard/', customer_dashboard, name='customer_dashboard'),
    path('create/item/', create_item, name='create_item'),
    path('edit/item/<int:pk>/', edit_item, name='edit_item'),
    path('create/discount/', create_discount, name='create_discount'),
    path('edit/discount/<int:pk>/', edit_discount, name='edit_discount'),
    path('logout/', user_logout, name='logout'),
    path('generate_bill/', generate_bill, name='generate_bill'),

]