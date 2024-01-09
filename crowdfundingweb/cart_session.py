from crowdfundingweb.models import Campania

CART_SESSION_ID = 'cart'

class ShoppingCartSession:

    """Inicializando el shopping cart"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    """Agregar item al cart"""
    def add(self, campania_id, aporte):
        campania_id = str(campania_id)
        
        if campania_id not in self.cart:
            self.cart[campania_id] = aporte
        else:
            self.cart[campania_id] += aporte
        
        self.save()


    """Actualizar cantidad de item en el cart"""
    def update(self, campania_id, aporte):
        campania_id = str(campania_id)

        if campania_id in self.cart:
            self.cart[campania_id] = aporte
        
        self.save()


    """Quitar item del cart"""
    def delete(self, campania_id):
        campania_id = str(campania_id)

        if campania_id in self.cart:
            del self.cart[campania_id]            
        self.save()


    def save(self):
        self.session.modified = True
        

    def clear(self):
        del self.session[CART_SESSION_ID]


    """Contabilizar todas las unidades agregadas al carrito"""
    def __len__(self):
        return sum(self.cart.values())
    
    """Obtener el detalle de campañas que están en el carrito"""
    def get_cart_detail(self):
        cart_items = []
        for campania_id, aporte in self.cart.items():
            campania = Campania.objects.get(pk=campania_id)
            cart_items.append({'campania': campania,
                               'aporte': aporte})
        return cart_items
    
    
    """Obtener el monto total de los items del carrito"""
    def get_total(self):        
        return sum(item['aporte'] for item in self.get_cart_detail())
    