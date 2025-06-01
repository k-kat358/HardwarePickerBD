from django.shortcuts import render,redirect, get_object_or_404
from .models import CPU,MOBO,CPUCooler,RAM,Storage,GPU,PSU,CASE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order, OrderItem
from django.db.models import Sum
from collections import defaultdict
import re

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
    # Initialize component slots
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

    # Populate main dict
    for item in cart_items:
        prod = item.product_object
        if not prod:
            continue
        if item.product_type in ['RAM', 'Storage']:
            components[item.product_type].append(prod)
        else:
            components[item.product_type] = prod

    cpu = components['CPU']; mobo = components['MOBO']; psu = components['PSU']
    case = components['CASE']; cooler = components['CPUCooler']; rams = components['RAM']
    gpu = components['GPU']; storages = components['Storage']

    def flag(ptype, pid, msg):
        '''Attach a compatibility message to all cart_items matching product type & id.'''
        for it in cart_items.filter(product_type=ptype, product_id=pid):
            compatibility_issues[it.id].append(msg)

    # Utility normalization and splitter
    def norm(val): return val.strip().lower() if isinstance(val, str) else val
    def split_multi(val):
        if not isinstance(val, str):
            return []
        parts = re.split(r'[\\/,\s]+', val)
        return [norm(p) for p in parts if p]

    # 1. CPU <-> Motherboard socket/platform
    if cpu and mobo:
        mobo_platforms = split_multi(mobo.platform)
        if norm(cpu.platform) not in mobo_platforms:
            msg = f"CPU socket ({cpu.platform}) doesn't match Motherboard ({mobo.platform})"
            flag('CPU', cpu.id, msg); flag('MOBO', mobo.id, msg)

    # 2. RAM <-> Motherboard type & capacity
    if mobo and rams:
        total_ram = sum(r.ram_capacity for r in rams)
        mobo_ram_types = split_multi(mobo.ram_type)
        for ram in rams:
            if norm(ram.ram_type) not in mobo_ram_types:
                msg = f"RAM type ({ram.ram_type}) not supported by motherboard ({mobo.ram_type})"
                flag('RAM', ram.id, msg)
        if total_ram > mobo.ram_capacity:
            msg = f"Total RAM ({total_ram}GB) exceeds motherboard max ({mobo.ram_capacity}GB)"
            for ram in rams: flag('RAM', ram.id, msg)

    # 3. Storage <-> M.2 slots
    if mobo and storages:
        nvme_count = sum(1 for s in storages if norm(s.interface) == 'nvme')
        if hasattr(mobo, 'm2_slots') and nvme_count > mobo.m2_slots:
            msg = f"NVMe drives ({nvme_count}) exceed motherboard M.2 slots ({mobo.m2_slots})"
            for s in storages: flag('Storage', s.id, msg)

    # 4. PSU power budgeting
    total_power = sum([
        cpu.power if cpu else 0,
        mobo.power if mobo else 0,
        sum(r.power for r in rams),
        sum(s.power for s in storages),
        gpu.power if gpu else 0,
    ])
    if psu and psu.capacity < total_power:
        msg = f"PSU capacity ({psu.capacity}W) insufficient for estimated draw ({total_power}W)"
        flag('PSU', psu.id, msg)

    # 5. Case <-> Motherboard form factor
    if case and mobo and hasattr(case, 'mobo_form_factor'):
        supported = split_multi(case.mobo_form_factor)
        if norm(mobo.mobo_form_factor) not in supported:
            msg = f"Case doesn't support {mobo.mobo_form_factor} motherboards"
            flag('CASE', case.id, msg)

    # 6. GPU <-> Case clearance
    if case and gpu and hasattr(case, 'max_gpu_length') and hasattr(gpu, 'length'):
        if gpu.length > case.max_gpu_length:
            msg = f"GPU length ({gpu.length}mm) exceeds case max ({case.max_gpu_length}mm)"
            flag('GPU', gpu.id, msg)
            flag('CASE', case.id, msg)

    # 7. Cooler <-> Case height & CPU socket
    if cooler and cpu:
        sup = split_multi(cooler.platform)
        if norm(cpu.platform) not in sup:
            msg = f"Cooler not compatible with {cpu.platform} socket"
            flag('CPUCooler', cooler.id, msg)
        if case and hasattr(case, 'max_cooler_height') and hasattr(cooler, 'height'):
            if cooler.height > case.max_cooler_height:
                msg = f"Cooler height ({cooler.height}mm) exceeds case limit ({case.max_cooler_height}mm)"
                flag('CPUCooler', cooler.id, msg); flag('CASE', case.id, msg)

    # 8. PSU size <-> Case PSU bay
    if psu and case and hasattr(psu, 'length') and hasattr(case, 'max_psu_length'):
        if psu.length > case.max_psu_length:
            msg = f"PSU length ({psu.length}mm) exceeds case PSU bay limit ({case.max_psu_length}mm)"
            flag('PSU', psu.id, msg); flag('CASE', case.id, msg)

    # Calculate total
    total_amount = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'compatibility_issues': dict(compatibility_issues),
    })
