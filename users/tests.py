from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Wishlist
from store.models import Product, Category
from decimal import Decimal

class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00'),
            available=True
        )

    def test_registration(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302) # Redirects after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302) # Redirects after successful login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302) # Redirects after successful logout
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_wishlist_add(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302) # Redirects after adding to wishlist
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_wishlist_remove(self):
        Wishlist.objects.create(user=self.user, product=self.product)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:remove_from_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302) # Redirects after removing from wishlist
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_wishlist_view(self):
        Wishlist.objects.create(user=self.user, product=self.product)
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/wishlist.html')
        self.assertContains(response, self.product.name)