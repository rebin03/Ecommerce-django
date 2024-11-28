
def cart_count_context(request):
    
    count = 0
    
    if request.user.is_authenticated:
        
        count = request.user.cart.cart_item.filter(is_order_placed=False).count()

    return {'item_count': count}