from django.test import TestCase
from store.models import Product, Category
from cart.cart import Cart
from decimal import Decimal

class CartTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Product 1',
            slug='product-1',
            price=Decimal('10.00'),
            available=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Product 2',
            slug='product-2',
            price=Decimal('20.00'),
            available=True
        )

    def test_cart_add(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=1)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.get_total_price(), Decimal('10.00'))

    def test_cart_add_multiple_items(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=2)
        cart.add(product=self.product2, quantity=1)
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.get_total_price(), Decimal('40.00'))

    def test_cart_add_override_quantity(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=1)
        cart.add(product=self.product1, quantity=5, override_quantity=True)
        self.assertEqual(len(cart), 5)
        self.assertEqual(cart.get_total_price(), Decimal('50.00'))

    def test_cart_remove(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=2)
        cart.remove(product=self.product1)
        self.assertEqual(len(cart), 0)
        self.assertEqual(cart.get_total_price(), Decimal('0.00'))

    def test_cart_clear(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=2)
        cart.add(product=self.product2, quantity=1)
        cart.clear()
        self.assertEqual(len(cart), 0)
        self.assertEqual(cart.get_total_price(), Decimal('0.00'))

    def test_cart_iter(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=1)
        cart.add(product=self.product2, quantity=2)
        
        items = list(cart)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['product'].name, 'Product 1')
        self.assertEqual(items[0]['quantity'], 1)
        self.assertEqual(items[1]['product'].name, 'Product 2')
        self.assertEqual(items[1]['quantity'], 2)

    def test_cart_get_total_price_after_discount_no_coupon(self):
        request = self.client.get('/').wsgi_request
        cart = Cart(request)
        cart.add(product=self.product1, quantity=1)
        self.assertEqual(cart.get_total_price_after_discount(), Decimal('10.00'))

    def test_cart_get_total_price_after_discount_with_coupon(self):
        from orders.models import Coupon
        from django.utils import timezone
        coupon = Coupon.objects.create(
            code='TEST10',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )
        request = self.client.get('/').wsgi_request
        request.session['coupon_id'] = coupon.id
        cart = Cart(request)
        cart.add(product=self.product1, quantity=1)
        self.assertEqual(cart.get_total_price_after_discount(), Decimal('9.00')) # 10% off of 10.00