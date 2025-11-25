from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from store.models import Category, Product, Review
from orders.models import Coupon
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates sample data for the store'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        fake = Faker()

        # Create Categories
        category_names = [
            'T-Shirts', 'Shirts', 'Jeans', 'Trousers', 'Dresses', 'Jackets', 'Sweaters', 'Skirts', 'Shorts'
        ]
        categories = []
        for name in category_names:
            category, created = Category.objects.get_or_create(name=name, slug=name.lower())
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))

        # Create Products
        clothing_names = [
            "Classic Cotton T-Shirt", "Slim Fit Denim Jeans", "V-Neck Cashmere Sweater", "Linen Button-Up Shirt",
            "Chino Trousers", "Floral Summer Dress", "Quilted Puffer Jacket", "Wool Blend Peacoat",
            "Graphic Print Hoodie", "Silk Camisole Top", "High-Waisted Skinny Jeans", "Pleated Midi Skirt",
            "Leather Biker Jacket", "Turtleneck Knit Sweater", "Denim Cut-off Shorts", "Bohemian Maxi Dress",
            "Striped Crewneck T-Shirt", "Corduroy Straight-Leg Pants", "Cable-Knit Cardigan", "Plaid Flannel Shirt",
            "Ankle-Grazer Trousers", "Ruffled Wrap Dress", "Faux Fur-Trimmed Parka", "Double-Breasted Trench Coat",
            "Embroidered Bomber Jacket", "Lace-Trimmed Slip Dress", "Distressed Boyfriend Jeans", "A-Line Denim Skirt",
            "Suede Moto Jacket", "Oversized Knit Jumper", "Drawstring Linen Shorts", "Polka Dot Sundress",
            "Vintage Wash T-Shirt", "Cropped Wide-Leg Jeans", "Chunky Knit-Turtleneck", "Utility Jumpsuit",
            "Sequin Party Dress", "Velvet Blazer", "Pinstripe Trousers", "Satin Midi Dress", "Tweed Mini Skirt",
            "Fringed Kimono", "Ribbed Tank Top", "Cargo Pants", "Cashmere Scarf", "Leather Gloves",
            "Fedora Hat", "Canvas Tote Bag"
        ]

        products = []
        for i in range(50):
            category = random.choice(categories)
            product_name = random.choice(clothing_names)
            slug = f"{product_name.lower().replace(' ', '-')}-{i}"
            product, created = Product.objects.get_or_create(
                category=category,
                name=product_name,
                slug=slug,
                defaults={
                    'description': fake.paragraph(nb_sentences=3),
                    'price': round(random.uniform(10.0, 100.0), 2),
                    'available': True
                }
            )
            products.append(product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product_name}'))

        # Create a Superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin'))

        # Create Reviews
        users = User.objects.all()
        if users.exists():
            for _ in range(100):
                product = random.choice(products)
                user = random.choice(users)
                rating = random.randint(1, 5)
                comment = fake.sentence()
                review, created = Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={'rating': rating, 'comment': comment}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created review for {product.name} by {user.username}'))

        # Create a sample Coupon
        coupon_code = "SAVE10"
        valid_from = timezone.now() - timezone.timedelta(days=1)
        valid_to = timezone.now() + timezone.timedelta(days=30)
        coupon, created = Coupon.objects.get_or_create(
            code=coupon_code,
            defaults={
                'valid_from': valid_from,
                'valid_to': valid_to,
                'discount': 10,
                'active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created coupon: {coupon_code}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation complete.'))
