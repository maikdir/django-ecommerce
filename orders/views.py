from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from store.models import Product # Import Product model from store app

def order_create(request):
    cart = Cart(request)
    if not cart: # Check if cart is empty
        return redirect('cart:cart_detail')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:payment') # Redirect to simulated payment
    else:
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            }
            form = OrderCreateForm(initial=initial_data)
        else:
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

def payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.paid = True
        order.save()
        return render(request, 'orders/order/created.html', {'order': order})

    return render(request, 'orders/order/payment.html', {'order': order})

@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = sum(order.get_total_cost() for order in Order.objects.filter(paid=True))
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="order_{order.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Order #{order.id}")

    # Customer Info
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Customer: {order.first_name} {order.last_name}")
    p.drawString(100, height - 100, f"Email: {order.email}")
    p.drawString(100, height - 120, f"Address: {order.address}, {order.city}, {order.postal_code}")
    p.drawString(100, height - 140, f"Date: {order.created.strftime('%Y-%m-%d')}")

    # Table Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 200, "Product")
    p.drawString(300, height - 200, "Price")
    p.drawString(400, height - 200, "Quantity")
    p.drawString(500, height - 200, "Total")
    p.line(100, height - 210, width - 100, height - 210)

    # Table Content
    p.setFont("Helvetica", 12)
    y = height - 230
    for item in order.items.all():
        p.drawString(100, y, item.product.name)
        p.drawString(300, y, f"${item.price}")
        p.drawString(400, y, str(item.quantity))
        p.drawString(500, y, f"${item.get_cost()}")
        y -= 20

    # Total
    p.line(100, y, width - 100, y)
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, y, "Total:")
    p.drawString(500, y, f"${order.get_total_cost()}")

    p.showPage()
    p.save()

    return response
