function addToCart(campaniaId,aporte,csrf_token) {

    const payload = {
        campania_id : campaniaId,
        aporte : aporte
    }

    fetch('/add-to-cart/', {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: {'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrf_token
                }
    })
    .then(res => res.json())
    .then(data =>document.getElementById('cart-items-counter').innerHTML = data.count_cart_items);
}

function removeFromCart(campaniaId,csrf_token){
    const payload={
        campania_id : campaniaId
    }

    fetch('/remove-from-cart/',{
        method:'POST',
        body: JSON.stringify(payload),
        headers: {'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrf_token
                }
    })
    .then(res=> res.json())
    .then(()=> location.href= '/cart'); 
}

function checkout(csrf_token){

    const payload={}

    fetch('/checkout/', {
        method : 'POST',
        bodybody: JSON.stringify(payload),
        headers: {'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrf_token
                }
    })
    .then(res=>{
        if (!res.ok){
            throw Error('El pedido no pudo ser registrado');
        }
        return res.json();
    })
    .then(data => {
        alert('se registra el pedido #' + data.codigo_pago);
        location.ref = '/'
    })
    .catch(error => alert(error));
}



