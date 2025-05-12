from django.shortcuts import render,redirect, get_object_or_404
from .models import CPU,MOBO,CPUCooler,RAM,Storage,GPU,PSU,CASE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order, OrderItem
from django.db.models import Sum
from collections import defaultdict

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, "order_list.html", {"orders": orders})

@login_required
def add_to_cart(request, product_type, product_id):
    product_model = {
        "CPU": CPU,
        "GPU": GPU,
        "RAM": RAM,
        "Storage": Storage,
        "PSU": PSU,
        "CASE": CASE,
        "MOBO": MOBO,
        "CPUCooler": CPUCooler,
    }.get(product_type)

    if not product_model:
        messages.error(request, "Invalid product type!")
        return redirect("home")

    product = get_object_or_404(product_model, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        product_id=product_id,
        defaults={"price": product.price, "quantity": 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect(product_type.lower())


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_amount": total_amount})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart_view")

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    total_amount = sum(item.total_price for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    for item in cart_items:
        product = item.product_object  # This uses your existing product_object property
        OrderItem.objects.create(
            order=order,
            product_type=item.product_type,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        )

    messages.success(request, f"Build #{order.id} saved successfully! You can continue adding more items.")
    return redirect("cart_view")


@login_required
def delete_order(request, order_id):
    # Ensure user can only delete their own orders
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Build deleted successfully!")
        return redirect('order_list')

    messages.error(request, "Invalid request method")
    return redirect('order_list')


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prepare order items with product details
    items_with_products = []
    for item in order.items.all():
        product = None
        model_map = {
            'CPU': CPU,
            'MOBO': MOBO,
            'CPUCooler': CPUCooler,
            'RAM': RAM,
            'Storage': Storage,
            'GPU': GPU,
            'PSU': PSU,
            'CASE': CASE,
        }
        model = model_map.get(item.product_type)
        if model:
            product = model.objects.filter(id=item.product_id).first()

        items_with_products.append({
            'item': item,
            'product': product
        })

    return render(request, "order_details.html", {
        "order": order,
        "items_with_products": items_with_products
    })

def cpu(request):
    cpu= CPU.objects.all()
    return render(request,'products/cpu.html',{'cpu':cpu})

def mobo(request):
    mobo= MOBO.objects.all()
    return render(request,'products/mobo.html',{'mobo':mobo})

def cpucooler(request):
    cpucooler= CPUCooler.objects.all()
    return render(request,'products/cpucooler.html',{'cpucooler':cpucooler})

def ram(request):
    ram= RAM.objects.all()
    return render(request,'products/ram.html',{'ram':ram})

def storage(request):
    storage= Storage.objects.all()
    return render(request,'products/storage.html',{'storage':storage})

def gpu(request):
    gpu= GPU.objects.all()
    return render(request,'products/gpu.html',{'gpu':gpu})

def case(request):
    case= CASE.objects.all()
    return render(request,'products/case.html',{'case':case})

def psu(request):
    psu= PSU.objects.all()
    return render(request,'products/psu.html',{'psu':psu})


def cpu_detail(request, cpu_id):
    cpu = get_object_or_404(CPU, id=cpu_id)
    return render(request, 'products/details.html', {'object': cpu})

def mobo_detail(request, mobo_id):
    mobo = get_object_or_404(MOBO, id=mobo_id)
    return render(request, 'products/details.html', {'object': mobo})

def cpu_cooler_detail(request, cooler_id):
    cooler = get_object_or_404(CPUCooler, id=cooler_id)
    return render(request, 'products/details.html', {'object': cooler})

def ram_detail(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    return render(request, 'products/details.html', {'object': ram})

def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id)
    return render(request, 'products/details.html', {'object': storage})

def gpu_detail(request, gpu_id):
    gpu = get_object_or_404(GPU, id=gpu_id)
    return render(request, 'products/details.html', {'object': gpu})

def psu_detail(request, psu_id):
    psu = get_object_or_404(PSU, id=psu_id)
    return render(request, 'products/details.html', {'object': psu})

def case_detail(request, case_id):
    case = get_object_or_404(CASE, id=case_id)
    return render(request, 'products/details.html', {'object': case})





# ... [Keep all your existing view functions above unchanged] ...

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    components = {
        'CPU': None,
        'MOBO': None,
        'RAM': [],
        'PSU': None,
        'CASE': None,
        'CPUCooler': None,
        'Storage': [],
        'GPU': None,
    }
    compatibility_issues = defaultdict(list)

    # Collect components from cart
    for item in cart_items:
        product = item.product_object
        if product:
            if item.product_type == 'CPU':
                components['CPU'] = product
            elif item.product_type == 'MOBO':
                components['MOBO'] = product
            elif item.product_type == 'RAM':
                components['RAM'].append(product)
            elif item.product_type == 'PSU':
                components['PSU'] = product
            elif item.product_type == 'CASE':
                components['CASE'] = product
            elif item.product_type == 'CPUCooler':
                components['CPUCooler'] = product
            elif item.product_type == 'Storage':
                components['Storage'].append(product)
            elif item.product_type == 'GPU':
                components['GPU'] = product

    # Compatibility checks
    cpu = components['CPU']
    mobo = components['MOBO']
    psu = components['PSU']
    case = components['CASE']
    cooler = components['CPUCooler']
    rams = components['RAM']
    gpu = components['GPU']
    storages = components['Storage']

    # CPU-Motherboard compatibility
    if cpu and mobo:
        if cpu.platform != mobo.platform:
            msg = f"CPU platform ({cpu.platform}) doesn't match Motherboard ({mobo.platform})"
            for item in cart_items:
                if item.product_type == 'CPU' and item.product_id == cpu.id:
                    compatibility_issues[item.id].append(msg)
                if item.product_type == 'MOBO' and item.product_id == mobo.id:
                    compatibility_issues[item.id].append(msg)

    # RAM-Motherboard compatibility
    if mobo and rams:
        for ram in rams:
            if ram.ram_type != mobo.ram_type:
                msg = f"RAM type ({ram.ram_type}) not supported by motherboard"
                for item in cart_items.filter(product_type='RAM', product_id=ram.id):
                    compatibility_issues[item.id].append(msg)

        total_ram = sum(ram.ram_capacity for ram in rams)
        if total_ram > mobo.ram_capacity:
            msg = f"Total RAM ({total_ram}GB) exceeds motherboard limit ({mobo.ram_capacity}GB)"
            for item in cart_items.filter(product_type='RAM'):
                compatibility_issues[item.id].append(msg)

    # PSU Wattage check
    total_power = sum([
        cpu.power if cpu else 0,
        mobo.power if mobo else 0,
        sum(ram.power for ram in rams),
        sum(storage.power for storage in storages),
        gpu.power if gpu else 0
    ])

    if psu and psu.capacity < total_power:
        msg = f"PSU capacity ({psu.capacity}W) insufficient for system ({total_power}W)"
        for item in cart_items.filter(product_type='PSU'):
            compatibility_issues[item.id].append(msg)

    # Case-Motherboard compatibility
    if case and mobo:
        if mobo.mobo_form_factor not in case.mobo_form_factor:
            msg = f"Case doesn't support {mobo.mobo_form_factor} motherboards"
            for item in cart_items.filter(product_type='CASE'):
                compatibility_issues[item.id].append(msg)

    # Cooler-CPU compatibility
    if cooler and cpu:
        if cpu.platform not in cooler.platform.split(', '):
            msg = f"Cooler not compatible with {cpu.platform} platform"
            for item in cart_items.filter(product_type='CPUCooler'):
                compatibility_issues[item.id].append(msg)

    total_amount = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'compatibility_issues': dict(compatibility_issues),
    }
    return render(request, "cart.html", context)
