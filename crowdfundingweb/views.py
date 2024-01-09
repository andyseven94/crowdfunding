from django.shortcuts import render
from django.shortcuts import render, redirect
from crowdfundingweb.models import Categoria, Campania, Contribucion
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .cart_session import ShoppingCartSession
import json
from django.http import JsonResponse
from django.db import transaction
import string,random



def home(request):
    campanias = Campania.objects.all()
    categoriasCampanias = Campania.categorias
    #contribuciones = Contribucion.objects.values('campania_id').annotate(Sum('monto_contribuido'))
    return render (request,'catalog.html', {'lista_campanias':campanias,
                                          'categorias_campanias' : categoriasCampanias,
                                            })

def do_signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username= username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Usuario o contrasena invalidos.')
        else:    
             messages.error(request, 'Usuario o contrasena invalidos.')
        
        
    form = AuthenticationForm()
    return render(request, 'signin.html',{'signin_form':form})

def do_logout(request):
    logout(request)
    return redirect('home')
    
def do_signup(request):
    if request.method == "POST":        
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            username = sign_up_form.cleaned_data.get('username')
            password = sign_up_form.cleaned_data.get('password1')
            nombre = sign_up_form.cleaned_data.get('nombre')
            apellido = sign_up_form.cleaned_data.get('apellido')
            email = sign_up_form.cleaned_data.get('email')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "El username ingresado ya está siendo utilizado!")
            else:            
                new_user = User(
                    username=username,
                    password=make_password(password),
                    is_superuser=False,
                    first_name=nombre,
                    last_name=apellido,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    date_joined=datetime.now()
                )
                new_user.save()             
                return redirect('success_signup')
    else:
        sign_up_form = SignUpForm()        
    
    return render(request, 'signup.html', {'sign_up_form': sign_up_form})

def success_signup(request):
    return render(request, 'success_signup.html')


def get_campanias_by_categoria(request, categoria_id):
    campanias = Campania.objects.filter(categorias__in=[categoria_id])
    return render(request, 'catalog.html',{'lista_campanias':campanias,
                                           })
    
def get_campanias_by_nombre(request, slug):
    campania = Campania.objects.filter(slug =slug).all()
    return render(request,'campanias.html', {'datos_campania':campania,
                                            })
    
def get_id_usuario(slug):
    usuario_id = Campania.objects.get(slug=slug).usuario
    return usuario_id

def add_to_cart(request):
    cart = ShoppingCartSession(request)
    payload = json.loads(request.body)
    
    campania_id = int(payload.get('campania_id'))
    aporte = int(payload.get('aporte'))
    
    try:
        campania_existente = Campania.objects.get(pk=campania_id)
        cart.add(campania_existente.id,aporte)
        return JsonResponse (status =200,data={'result':True, 'message':'OK', 'count_cart_items': cart.__len__()})
    except Campania.DoesNotExist:
        return JsonResponse (status=404, data={'result': False ,'message': 'No se encontró la campaña'})
        
def remove_from_cart(request):
    cart = ShoppingCartSession(request)
    payload = json.loads(request.body)
    campania_id = int(payload.get('campania_id'))
    cart.delete(campania_id)
    return JsonResponse (status =200,data={'result':True, 'message':'OK', 'count_cart_items': cart.__len__()})

def get_shopping_cart(request):
    cart = ShoppingCartSession(request)
    return render(request,'cart.html',{'cart':cart.get_cart_detail(),
                                        'count_cart_items': cart.__len__(),
                                        'cart_total':cart.get_total(),
                                        }) 
    
@transaction.atomic
def checkout(request):
    cart = ShoppingCartSession(request)
    try:
        
        #generacion de pago
        #total = cart.get_total()
        codigo_pago = generar_codigo_pedido()
        
        for item in cart.get_cart_detail():
            print(item)
            print(item.get('aporte'))
            campania = item.get('campania')
            contribucion = Contribucion(
                usuario = request.user,
                #codigo= generar_codigo_pedido(),
                campania_id= campania,
                monto_contribuido = item.get('aporte'),
                fecha_contribucion = datetime.now(),
                comentario_contribucion ='dato quemado en views'
            )
            contribucion.save()
            print("exito contribucion")
            
        cart.clear()
        return JsonResponse(status=200, data={'codigo_pedido':codigo_pago})        
    except Exception as error:
        print(error)
        return JsonResponse(status= 500, data={'error_msg':f'No se pudo generar el pago. Error:{error}'})
        
def generar_codigo_pedido():
    caracteres = string.ascii_letters + string.digits
    codigo_pedido = 'PED-' + ''.join(random.choice(caracteres) for _ in range(5))
    return codigo_pedido
    
