from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Product, Category
from orders.models import Order, OrderItem, Coupon
from decimal import Decimal
from django.utils import timezone

class OrderTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00'),
            available=True
        )
        self.coupon = Coupon.objects.create(
            code='TESTCOUPON',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )

    def test_order_creation_no_coupon(self):
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {'quantity': 1, 'price': str(self.product.price)}
        }
        session.save()

        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Anytown'
        })

        self.assertEqual(response.status_code, 303) # Redirect to payment
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.get_total_cost(), Decimal('10.00'))

    def test_order_creation_with_coupon(self):
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {'quantity': 1, 'price': str(self.product.price)}
        }
        session['coupon_id'] = self.coupon.id
        session.save()

        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'address': '456 Oak Ave',
            'postal_code': '67890',
            'city': 'Otherville'
        })
        
        self.assertEqual(response.status_code, 303) # Redirect to payment
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.coupon, self.coupon)
        self.assertEqual(order.discount, 10)
        self.assertEqual(order.get_total_cost(), Decimal('9.00')) # 10% off of 10.00

    def test_payment_completed(self):
        order = Order.objects.create(
            user=self.user,
            first_name='Test', last_name='User', email='test@example.com',
            address='123 Test St', postal_code='11111', city='Test City', paid=False
        )
        self.client.session['order_id'] = order.id
        self.client.session.save()
        
        response = self.client.get(reverse('orders:payment_completed'))
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertTrue(order.paid)
        self.assertTemplateUsed(response, 'orders/order/created.html')

    def test_payment_canceled(self):
        response = self.client.get(reverse('orders:payment_canceled'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/canceled.html')

    def test_admin_dashboard_access(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('orders:admin_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect non-staff

        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('orders:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/dashboard.html')

    def test_admin_dashboard_data(self):
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')

        order = Order.objects.create(
            user=self.user,
            first_name='Test', last_name='User', email='test@example.com',
            address='123 Test St', postal_code='11111', city='Test City', paid=True
        )
        OrderItem.objects.create(order=order, product=self.product, price=self.product.price, quantity=1)

        response = self.client.get(reverse('orders:admin_dashboard'))
        self.assertContains(response, '1') # Total Products
        self.assertContains(response, '1') # Total Orders
        self.assertContains(response, '10.00') # Total Revenue

    def test_admin_order_pdf_access(self):
        order = Order.objects.create(
            user=self.user,
            first_name='Test', last_name='User', email='test@example.com',
            address='123 Test St', postal_code='11111', city='Test City', paid=True
        )
        OrderItem.objects.create(order=order, product=self.product, price=self.product.price, quantity=1)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('orders:admin_order_pdf', args=[order.id]))
        self.assertEqual(response.status_code, 302) # Redirect non-staff

        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('orders:admin_order_pdf', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')