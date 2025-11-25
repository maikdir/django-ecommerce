from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product, Review
from decimal import Decimal

class StoreModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='T-Shirts', slug='t-shirts')
        self.product = Product.objects.create(
            category=self.category,
            name='Test T-Shirt',
            slug='test-t-shirt',
            description='A test t-shirt',
            price=Decimal('19.99'),
            available=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'T-Shirts')
        self.assertEqual(self.category.slug, 't-shirts')
        self.assertEqual(str(self.category), 'T-Shirts')
        self.assertEqual(self.category.get_absolute_url(), '/t-shirts/')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test T-Shirt')
        self.assertEqual(self.product.slug, 'test-t-shirt')
        self.assertEqual(self.product.price, Decimal('19.99'))
        self.assertTrue(self.product.available)
        self.assertEqual(str(self.product), 'Test T-Shirt')
        self.assertEqual(self.product.get_absolute_url(), f'/{self.product.id}/test-t-shirt/')

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Great product!'
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product!')
        self.assertEqual(str(review), f'Review by {self.user} on {self.product}')
        self.assertEqual(self.product.rating, 5.0) # Check if product rating is updated

    def test_product_rating_update(self):
        Review.objects.create(product=self.product, user=self.user, rating=4, comment='Good')
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 4.0)

        user2 = User.objects.create_user(username='testuser2', password='password')
        Review.objects.create(product=self.product, user=user2, rating=2, comment='Bad')
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 3.0) # (4+2)/2

    def test_product_rating_delete_review(self):
        review1 = Review.objects.create(product=self.product, user=self.user, rating=4, comment='Good')
        user2 = User.objects.create_user(username='testuser2', password='password')
        review2 = Review.objects.create(product=self.product, user=user2, rating=2, comment='Bad')

        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 3.0)

        review1.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 2.0)