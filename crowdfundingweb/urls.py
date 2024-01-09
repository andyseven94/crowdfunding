from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.do_signin , name = 'signin'),
    path('logout/', views.do_logout, name = 'logout'),
    path('signup/', views.do_signup, name = 'signup'),
    path('success_signup', views.success_signup, name ='success_signup'),   
    path('categorias/<int:categoria_id>/campanias/', views.get_campanias_by_categoria, name='campanias_por_categoria'),
    path('campanias/<str:slug>', views.get_campanias_by_nombre, name = 'campanias_por_nombre'),
    path('add-to-cart/', views.add_to_cart, name= 'add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name ='remove_from_cart'),
    path('cart/', views.get_shopping_cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
]